import asyncio
import os
import threading
import signal
import sys
import time
from collections import defaultdict
from typing import List
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from models import Opportunity
from fetcher import AsyncFetcher
from web_dashboard import start_flask_app, update_dashboard_data
from notifier import TelegramNotifier

load_dotenv()
console = Console()

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 0))
MIN_SPREAD = float(os.getenv("MIN_SPREAD", 0.025))

class ArbitrageBot:
    def __init__(self):
        self.fetcher = AsyncFetcher(USER_AGENT)
        self.notifier = TelegramNotifier()
        self.running = True
        self.latest_opportunities: List[Opportunity] = []

    def calculate_arbitrage(self, rates: List) -> List[Opportunity]:
        # Fast grouping using dict of lists
        grouped = defaultdict(list)
        norm = str.replace
        for r in rates:
            # Inline normalize — avoid function call overhead
            s = r.symbol
            s = s.replace('-', '').replace('_', '').replace('/', '').upper()
            if s.endswith('USDT'):
                grouped[s].append(r)

        opps = []
        append = opps.append
        ms = MIN_SPREAD
        for symbol, entries in grouped.items():
            # Fast unique by exchange
            if len(entries) < 2:
                continue
            seen = {}
            for e in entries:
                seen[e.exchange] = e  # Last wins (dedup)
            unique = list(seen.values())
            if len(unique) < 2:
                continue

            # Sort only if needed — use min/max instead of full sort
            long = unique[0]
            short = unique[0]
            for e in unique[1:]:
                if e.rate < long.rate:
                    long = e
                if e.rate > short.rate:
                    short = e

            spread = short.rate - long.rate
            if spread >= ms:
                append(Opportunity(
                    symbol=symbol,
                    long_exchange=long.exchange,
                    long_rate=long.rate,
                    short_exchange=short.exchange,
                    short_rate=short.rate,
                    spread=spread,
                    annualized_spread=spread * 3 * 365
                ))

        opps.sort(key=lambda x: x.spread, reverse=True)
        return opps

    async def run_loop(self):
        await self.fetcher.start_session()
        console.print(Panel.fit("[bold green]🚀 Arbitrage Engine Active[/bold green] [bold cyan]20 Exchanges • <250ms Latency[/bold cyan]", border_style="green"))

        while self.running:
            start_ns = time.perf_counter_ns()

            # 1. Fetch all 20 exchanges in parallel (200ms timeout each)
            all_rates = await self.fetcher.fetch_all()

            # 2. Calculate arbitrage
            total_pairs = len(set(r.symbol for r in all_rates))
            self.latest_opportunities = self.calculate_arbitrage(all_rates)

            # 3. Update dashboard & notify concurrently
            update_dashboard_data(self.latest_opportunities, total_pairs)
            await self.notifier.process(self.latest_opportunities)

            elapsed_ns = time.perf_counter_ns() - start_ns
            elapsed_ms = elapsed_ns / 1_000_000
            elapsed_s = elapsed_ns / 1_000_000_000

            # 4. Output
            self._print_dashboard(len(all_rates), total_pairs, len(self.latest_opportunities), elapsed_ms)

            # 5. Sleep to maintain interval (sub-ms precision)
            sleep_time = max(0, FETCH_INTERVAL - elapsed_s)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    def _print_dashboard(self, total_rates, total_pairs, opp_count, latency_ms):
        # Latency color
        if latency_ms < 250:
            latency_style = "bold green"
        elif latency_ms < 500:
            latency_style = "bold yellow"
        else:
            latency_style = "bold red"

        summary = Table(box=box.SIMPLE, show_header=False)
        summary.add_column("Key", style="cyan")
        summary.add_column("Val", style="bold white")
        summary.add_row("⏱️ Latency", f"[{latency_style}]{latency_ms:.1f}ms[/{latency_style}]")
        summary.add_row("📡 Points", f"{total_rates}")
        summary.add_row("🔄 Pairs", f"{total_pairs}")
        summary.add_row("🏦 Exchanges", "20")

        # Display Table with REAL spread
        opp_table = Table(title="🏆 TOP OPPORTUNITIES (Per Round)", box=box.ROUNDED)
        opp_table.add_column("#", style="yellow")
        opp_table.add_column("Pair", style="bold white")
        opp_table.add_column("Spread", justify="right", style="bold green")
        opp_table.add_column("Long (Buy)", style="blue")
        opp_table.add_column("Short (Sell)", style="red")

        for i, o in enumerate(self.latest_opportunities[:10], 1):
            opp_table.add_row(
                str(i),
                o.symbol,
                f"{o.spread:.4f}%",
                f"{o.long_exchange} ({o.long_rate:.4f}%)",
                f"{o.short_exchange} ({o.short_rate:.4f}%)"
            )

        console.print(Panel(summary, title="Status"))
        if self.latest_opportunities:
            console.print(opp_table)

    async def close(self):
        await self.fetcher.close()

def signal_handler(sig, frame):
    print("\n[INFO] Shutting down...")
    sys.exit(0)

async def main():
    bot = ArbitrageBot()
    try:
        await bot.run_loop()
    finally:
        await bot.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()

    # Start Async Loop with uvloop on Linux
    try:
        if sys.platform != 'win32':
            import uvloop
            uvloop.install()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
