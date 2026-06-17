import asyncio
import aiohttp
import logging
import time
from typing import List, Any
from models import FundingRate

logger = logging.getLogger("Fetcher")
logger.setLevel(logging.INFO)

# Per-exchange timeout in seconds — asyncio.gather runs all exchanges in parallel,
# so total wall-clock time is ~max(individual latencies), NOT sum of all latencies.
# If an exchange takes >10s, it gets cancelled and returns empty for that cycle.
EXCHANGE_TIMEOUT = 10.0  # 10s per exchange (accommodates real-world network latency)

# Session-level limits
SESSION_CONNECTOR_LIMIT = 128       # Max simultaneous connections
SESSION_CONNECTOR_LIMIT_PER_HOST = 16 # Max per host (prevents socket flooding)
DNS_CACHE_TTL = 600                 # 10 min DNS cache
SESSION_TOTAL_TIMEOUT = 15          # 15s total session timeout
SESSION_CONNECT_TIMEOUT = 5         # 5s TCP connect timeout

class AsyncFetcher:
    def __init__(self, user_agent: str):
        self.std_headers = {
            'User-Agent': 'python-requests/2.31.0',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
        }
        self.browser_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Origin': 'https://www.google.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }
        self.session = None
        # Cached instrument lists (refreshed every 30 minutes)
        self._cryptocom_instruments = []
        self._cryptocom_instruments_ts = 0
        self._poloniex_instruments = []
        self._poloniex_instruments_ts = 0
        # Concurrency limiter — prevent connection pool exhaustion
        self._fetch_semaphore = asyncio.Semaphore(10)

    async def start_session(self):
        connector = aiohttp.TCPConnector(
            limit=SESSION_CONNECTOR_LIMIT,
            limit_per_host=SESSION_CONNECTOR_LIMIT_PER_HOST,
            ttl_dns_cache=DNS_CACHE_TTL,
            ssl=False,
            enable_cleanup_closed=True,
            force_close=False,  # Reuse connections (HTTP keep-alive)
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(
                total=SESSION_TOTAL_TIMEOUT,
                connect=SESSION_CONNECT_TIMEOUT,
                sock_connect=SESSION_CONNECT_TIMEOUT,
                sock_read=5,  # 5s max wait for response body
            ),
            skip_auto_headers=['Accept-Encoding'],  # Don't send accept-encoding
        )

    async def close(self):
        if self.session:
            await self.session.close()

    async def _fetch(self, url: str, mode: str = 'std', extra_headers: dict = None, method: str = 'GET', post_data: dict = None) -> Any:
        if not self.session:
            return None
        headers = self.browser_headers if mode == 'browser' else self.std_headers
        if extra_headers:
            headers = {**headers, **extra_headers}

        try:
            if method == 'POST':
                if 'Content-Type' not in headers:
                    headers = {**headers, 'Content-Type': 'application/json'}
                async with self.session.post(url, headers=headers, json=post_data, ssl=False) as response:
                    if response.status == 200:
                        return await response.json(content_type=None)
            else:
                async with self.session.get(url, headers=headers, ssl=False) as response:
                    if response.status == 200:
                        return await response.json(content_type=None)
            return None
        except Exception:
            return None

    def _norm(self, symbol: str) -> str:
        return symbol.replace('-', '').replace('_', '').replace('/', '').upper()

    # EXCHANGE FETCHERS

    async def get_binance(self) -> List[FundingRate]:
        data = await self._fetch("https://fapi.binance.com/fapi/v1/premiumIndex", mode='browser')
        if not data:
            return []
        res, ts = [], time.time()
        for i in data:
            if i.get('symbol', '').endswith('USDT'):
                try:
                    res.append(FundingRate(exchange="Binance", symbol=i['symbol'], rate=float(i['lastFundingRate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_bybit(self) -> List[FundingRate]:
        data = await self._fetch("https://api.bybit.com/v5/market/tickers?category=linear", mode='browser')
        if not data or data.get('retCode') != 0:
            return []
        res, ts = [], time.time()
        for i in data.get('result', {}).get('list', []):
            if i.get('symbol', '').endswith('USDT') and i.get('fundingRate'):
                try:
                    res.append(FundingRate(exchange="Bybit", symbol=i['symbol'], rate=float(i['fundingRate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_gateio(self) -> List[FundingRate]:
        data = await self._fetch("https://api.gateio.ws/api/v4/futures/usdt/tickers", mode='std')
        if not data:
            return []
        res, ts = [], time.time()
        for i in data:
            if 'contract' in i and 'funding_rate' in i:
                try:
                    res.append(FundingRate(exchange="GateIO", symbol=self._norm(i['contract']), rate=float(i['funding_rate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_okx(self) -> List[FundingRate]:
        """Delta Exchange — USD-settled perpetual futures with funding rate."""
        url = "https://api.india.delta.exchange/v2/tickers?contract_types=perpetual_futures"
        data = await self._fetch(url, mode='std')
        if not data or 'result' not in data:
            return []
        res, ts = [], time.time()
        for i in data['result']:
            if i.get('contract_type') != 'perpetual_futures':
                continue
            rate = i.get('funding_rate')
            sym = i.get('symbol', '')
            if rate is not None and sym:
                try:
                    norm = sym.replace('-', '').upper()
                    res.append(FundingRate(exchange="DeltaExchange", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_kucoin(self) -> List[FundingRate]:
        data = await self._fetch("https://api-futures.kucoin.com/api/v1/contracts/active", mode='std')
        if not data or data.get('code') != '200000':
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            if i.get('symbol', '').endswith('USDTM') and i.get('fundingFeeRate'):
                try:
                    res.append(FundingRate(exchange="KuCoin", symbol=i['symbol'].replace('USDTM', 'USDT'), rate=float(i['fundingFeeRate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_bitget(self) -> List[FundingRate]:
        data = await self._fetch("https://api.bitget.com/api/v2/mix/market/tickers?productType=USDT-FUTURES", mode='std')
        if not data or data.get('code') != '00000':
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            if i.get('symbol', '').endswith('USDT') and i.get('fundingRate'):
                try:
                    res.append(FundingRate(exchange="Bitget", symbol=i['symbol'], rate=float(i['fundingRate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_mexc(self) -> List[FundingRate]:
        data = await self._fetch("https://contract.mexc.com/api/v1/contract/ticker", mode='std')
        if not data or not data.get('success'):
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            if i.get('symbol', '').endswith('_USDT') and i.get('fundingRate'):
                try:
                    res.append(FundingRate(exchange="MEXC", symbol=self._norm(i['symbol']), rate=float(i['fundingRate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_huobi(self) -> List[FundingRate]:
        url = "https://api.hbdm.vn/linear-swap-api/v1/swap_batch_funding_rate"
        data = await self._fetch(url, mode='std')
        if not data or data.get('status') != 'ok':
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            if i.get('contract_code', '').endswith('USDT') and i.get('funding_rate'):
                try:
                    res.append(FundingRate(exchange="Huobi", symbol=self._norm(i['contract_code']), rate=float(i['funding_rate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_bingx(self) -> List[FundingRate]:
        data = await self._fetch("https://open-api.bingx.com/openApi/swap/v2/quote/premiumIndex", mode='std')
        if not data or data.get('code') != 0:
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            rate_val = i.get('lastFundingRate')
            if i.get('symbol', '').endswith('-USDT') and rate_val:
                try:
                    res.append(FundingRate(exchange="BingX", symbol=self._norm(i['symbol']), rate=float(rate_val) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_kraken(self) -> List[FundingRate]:
        data = await self._fetch("https://futures.kraken.com/derivatives/api/v3/tickers", mode='std')
        if not data or data.get('result') != 'success':
            return []
        res, ts = [], time.time()
        seen = set()
        for i in data.get('tickers', []):
            sym = i.get('symbol', '').upper()
            if 'USD' not in sym or 'fundingRate' not in i:
                continue
            if "XBT" in sym:
                norm = "BTCUSDT"
            elif "ETH" in sym:
                norm = "ETHUSDT"
            else:
                norm = sym.replace('PF_', '').replace('USD', '') + "USDT"
            if norm in seen:
                continue
            seen.add(norm)
            try:
                res.append(FundingRate(exchange="Kraken", symbol=norm, rate=float(i['fundingRate']), timestamp=ts))
            except (ValueError, KeyError):
                continue
        return res

    async def get_dydx(self) -> List[FundingRate]:
        data = await self._fetch("https://indexer.dydx.trade/v4/perpetualMarkets", mode='std')
        if not data or 'markets' not in data:
            return []
        res, ts = [], time.time()
        for key, i in data['markets'].items():
            if i.get('nextFundingRate'):
                try:
                    symbol = i.get('ticker', key).replace('-USD', 'USDT')
                    rate = float(i['nextFundingRate']) * 100
                    res.append(FundingRate(exchange="dYdX", symbol=symbol, rate=rate, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_bitmex(self) -> List[FundingRate]:
        """Blofin — USDT perpetual futures with funding rate."""
        url = "https://openapi.blofin.com/api/v1/market/funding-rate?instType=swap"
        data = await self._fetch(url, mode='std')
        if not data or 'data' not in data:
            return []
        res, ts = [], time.time()
        for i in data['data']:
            inst_id = i.get('instId', '')
            rate = i.get('fundingRate')
            if inst_id.endswith('USDT') and rate is not None:
                try:
                    norm = inst_id.replace('-', '').upper()
                    res.append(FundingRate(exchange="Blofin", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_phemex(self) -> List[FundingRate]:
        """Deribit — BTC and ETH perpetual futures with funding rate."""
        res, ts = [], time.time()
        for sym in ["BTC-PERPETUAL", "ETH-PERPETUAL"]:
            data = await self._fetch(
                f"https://www.deribit.com/api/v2/public/ticker?instrument_name={sym}",
                mode='std'
            )
            if not data or 'result' not in data:
                continue
            r = data['result']
            rate = r.get('funding_8h')
            name = r.get('instrument_name', '')
            if rate is not None and name:
                try:
                    norm = name.replace('-', '').replace('PERPETUAL', 'USDT')
                    res.append(FundingRate(exchange="Deribit", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_htx(self) -> List[FundingRate]:
        url = "https://api.hbdm.com/linear-swap-api/v1/swap_batch_funding_rate"
        data = await self._fetch(url, mode='std')
        if not data or data.get('status') != 'ok':
            return []
        res, ts = [], time.time()
        for i in data.get('data', []):
            if i.get('contract_code', '').endswith('USDT') and i.get('funding_rate'):
                try:
                    res.append(FundingRate(exchange="HTX", symbol=self._norm(i['contract_code']), rate=float(i['funding_rate']) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_crypto_com(self) -> List[FundingRate]:
        """CryptoCom — fetch instruments once, then batch top funding rates."""
        now = time.time()
        # Refresh instrument list every 30 minutes
        if not self._cryptocom_instruments or (now - self._cryptocom_instruments_ts) > 1800:
            inst_data = await self._fetch(
                "https://deriv-api.crypto.com/v1/public/get-instruments?instrument_type=FUTURES",
                mode='std'
            )
            if inst_data and inst_data.get('code') == 0:
                instruments = inst_data.get('result', {}).get('data', [])
                self._cryptocom_instruments = [
                    i['symbol'] for i in instruments
                    if 'PERP' in i.get('symbol', '')
                ]
                self._cryptocom_instruments_ts = now

        if not self._cryptocom_instruments:
            return []

        # Fetch funding rates in parallel — limit to 50 instruments to stay within timeout
        instruments = self._cryptocom_instruments[:50]

        async def fetch_one(sym):
            try:
                url = f"https://deriv-api.crypto.com/v1/public/get-valuations?valuation_type=funding_rate&instrument_name={sym}"
                data = await self._fetch(url, mode='std')
                if data and data.get('code') == 0:
                    points = data.get('result', {}).get('data', [])
                    if points:
                        return (sym, points[0].get('v'))
            except Exception:
                pass
            return (sym, None)

        results = await asyncio.gather(
            *[fetch_one(s) for s in instruments],
            return_exceptions=True
        )

        res, ts = [], time.time()
        for r in results:
            if isinstance(r, tuple) and len(r) == 2:
                sym, rate = r
                if rate is not None:
                    try:
                        norm = sym.replace('-', '').replace('_PERP', '').upper()
                        res.append(FundingRate(exchange="CryptoCom", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                    except (ValueError, KeyError):
                        continue
        return res

    async def get_coinbase(self) -> List[FundingRate]:
        res, ts = [], time.time()
        # Try main API first (returns dict with products)
        data = await self._fetch(
            "https://api.coinbase.com/api/v3/brokerage/market/products?product_type=FUTURE",
            mode='browser'
        )
        if data and isinstance(data, dict):
            for p in data.get('products', []):
                details = p.get('future_product_details', {})
                perpetual = details.get('perpetual_details', {})
                rate = perpetual.get('funding_rate') or details.get('funding_rate')
                if rate:
                    try:
                        product_id = p.get('product_id', '')
                        norm = product_id.replace('BIP-', '').replace('-USDT', 'USDT').replace('-', '')
                        if not norm.endswith('USDT'):
                            norm = norm + 'USDT'
                        res.append(FundingRate(exchange="Coinbase", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                    except (ValueError, KeyError):
                        continue
        return res

    async def get_hyperliquid(self) -> List[FundingRate]:
        url = "https://api.hyperliquid.xyz/info"
        post_body = {"type": "metaAndAssetCtxs"}
        data = await self._fetch(url, mode='std', method='POST', post_data=post_body)
        if not data or not isinstance(data, list) or len(data) < 2:
            return []
        universe = data[0].get('universe', []) if isinstance(data[0], dict) else data[0]
        ctxs = data[1]
        res, ts = [], time.time()
        if len(universe) != len(ctxs):
            return []
        for u, c in zip(universe, ctxs):
            try:
                name = u.get('name')
                funding = c.get('funding')
                if name and funding:
                    symbol = f"{name}USDT"
                    res.append(FundingRate(exchange="Hyperliquid", symbol=symbol, rate=float(funding) * 100, timestamp=ts))
            except (ValueError, KeyError):
                continue
        return res

    async def get_coinex(self) -> List[FundingRate]:
        url = "https://api.coinex.com/perpetual/v1/market/ticker/all"
        data = await self._fetch(url, mode='std')
        if not data or data.get('code') != 0:
            return []
        ticker_data = data.get('data', {}).get('ticker', {})
        res, ts = [], time.time()
        for sym, details in ticker_data.items():
            rate = details.get('funding_rate_next') or details.get('funding_rate_last')
            if sym.endswith('USDT') and rate:
                try:
                    res.append(FundingRate(exchange="CoinEx", symbol=sym, rate=float(rate) * 100, timestamp=ts))
                except (ValueError, KeyError):
                    continue
        return res

    async def get_bitunix(self) -> List[FundingRate]:
        url = "https://fapi.bitunix.com/api/v1/futures/market/funding_rate/batch"
        data = await self._fetch(url, mode='std')
        res, ts = [], time.time()
        if data and data.get('code') == 0:
            for i in data.get('data', []):
                if i.get('symbol', '').endswith('USDT') and i.get('fundingRate'):
                    try:
                        res.append(FundingRate(exchange="BitUnix", symbol=i['symbol'], rate=float(i['fundingRate']), timestamp=ts))
                    except (ValueError, KeyError):
                        continue
        if not res:
            url_ticker = "https://fapi.bitunix.com/api/v1/futures/market/tickers"
            data_t = await self._fetch(url_ticker, mode='std')
            if data_t and data_t.get('code') == 0:
                for i in data_t.get('data', []):
                    if i.get('symbol', '').endswith('USDT') and i.get('fundingRate'):
                        try:
                            res.append(FundingRate(exchange="BitUnix", symbol=i['symbol'], rate=float(i['fundingRate']), timestamp=ts))
                        except (ValueError, KeyError):
                            continue
        return res

    async def get_poloniex(self) -> List[FundingRate]:
        """Poloniex — v3 API with cached instruments and parallel funding rates."""
        now = time.time()
        # Refresh instrument list every 30 minutes
        if not self._poloniex_instruments or (now - self._poloniex_instruments_ts) > 1800:
            inst_data = await self._fetch(
                "https://api.poloniex.com/v3/market/allInstruments",
                mode='std'
            )
            if inst_data and inst_data.get('code') == 200:
                instruments = inst_data.get('data', [])
                self._poloniex_instruments = [
                    i['symbol'] for i in instruments
                    if i.get('ctType') == 'LINEAR' and i.get('qCcy') == 'USDT'
                ]
                self._poloniex_instruments_ts = now

        if not self._poloniex_instruments:
            return []

        # Fetch funding rates in parallel
        async def fetch_one(sym):
            try:
                url = f"https://api.poloniex.com/v3/market/fundingRate?symbol={sym}"
                data = await self._fetch(url, mode='std')
                if data and data.get('code') == 200:
                    d = data.get('data', {})
                    return (sym, d.get('fR'))
            except Exception:
                pass
            return (sym, None)

        results = await asyncio.gather(
            *[fetch_one(s) for s in self._poloniex_instruments],
            return_exceptions=True
        )

        res, ts = [], time.time()
        for r in results:
            if isinstance(r, tuple) and len(r) == 2:
                sym, rate = r
                if rate is not None:
                    try:
                        norm = sym.replace('_', '').replace('PERP', '').upper()
                        res.append(FundingRate(exchange="Poloniex", symbol=norm, rate=float(rate) * 100, timestamp=ts))
                    except (ValueError, KeyError):
                        continue
        return res

    # PARALLEL FETCH ENGINE

    async def _fetch_exchange_with_timeout(self, name: str, coro) -> tuple:
        """Run a single exchange fetch with a strict per-exchange timeout."""
        try:
            result = await asyncio.wait_for(coro, timeout=EXCHANGE_TIMEOUT)
            return (name, result)
        except (asyncio.TimeoutError, Exception) as e:
            return (name, [])

    async def fetch_all(self) -> List[FundingRate]:
        if not self.session:
            await self.start_session()

        # All 20 exchanges — every single one MUST be here
        tasks = {
            "Binance":      self.get_binance(),
            "Bybit":        self.get_bybit(),
            "DeltaExchange": self.get_okx(),
            "GateIO":       self.get_gateio(),
            "KuCoin":       self.get_kucoin(),
            "Bitget":       self.get_bitget(),
            "MEXC":         self.get_mexc(),
            "Huobi":        self.get_huobi(),
            "BingX":        self.get_bingx(),
            "Kraken":       self.get_kraken(),
            "dYdX":         self.get_dydx(),
            "Blofin":       self.get_bitmex(),
            "Deribit":      self.get_phemex(),
            "HTX":          self.get_htx(),
            "CryptoCom":    self.get_crypto_com(),
            "Coinbase":     self.get_coinbase(),
            "Hyperliquid":  self.get_hyperliquid(),
            "CoinEx":       self.get_coinex(),
            "BitUnix":      self.get_bitunix(),
            "Poloniex":     self.get_poloniex(),
        }

        # Wrap each task with per-exchange timeout
        timeout_tasks = [
            self._fetch_exchange_with_timeout(name, coro)
            for name, coro in tasks.items()
        ]

        # Run ALL 20 exchanges in parallel with gather
        results = await asyncio.gather(*timeout_tasks, return_exceptions=False)

        flat_results = []
        debug_stats = {}
        for name, res in results:
            if isinstance(res, list):
                count = len(res)
                debug_stats[name] = count
                flat_results.extend(res)
            else:
                debug_stats[name] = "ERR"

        # Compact Report
        print("\n🔍 FETCH REPORT:")
        for name, count in debug_stats.items():
            status = f"[green]✅ {count}[/green]" if isinstance(count, int) and count > 0 else f"[red]❌ {count}[/red]"
            print(f"   {name:12s}: {status}")
        return flat_results
