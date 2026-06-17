<div align="center">

# ⚡ ATHENA ⚡

### Real-Time Multi-Exchange Funding Rate Arbitrage System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Async](https://img.shields.io/badge/Async-aiohttp-2C5BB4?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Exchanges](https://img.shields.io/badge/Exchanges-20-ef4444?style=for-the-badge&logo=bitcoin&logoColor=white)](#-supported-exchanges)

<br/>

<img src="https://img.shields.io/badge/⚡_Real--Time_Scanning-Active-10b981?style=flat-square" />
<img src="https://img.shields.io/badge/📡_Parallel_Fetch-asyncio.gather-6366f1?style=flat-square" />
<img src="https://img.shields.io/badge/🤖_Telegram_Alerts-Enabled-06b6d4?style=flat-square" />
<img src="https://img.shields.io/badge/🐳_Docker_Ready-2496ED?style=flat-square&logo=docker&logoColor=white" />

<br/><br/>
<p align="center">
<pre>
    █████╗ ████████╗██╗  ██╗███████╗███╗   ██╗ █████╗ 
   ██╔══██╗╚══██╔══╝██║  ██║██╔════╝████╗  ██║██╔══██╗
   ███████║   ██║   ███████║█████╗  ██╔██╗ ██║███████║
   ██╔══██║   ██║   ██╔══██║██╔══╝  ██║╚██╗██║██╔══██║
   ██║  ██║   ██║   ██║  ██║███████╗██║ ╚████║██║  ██║
   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                                       
   ⚡ Funding Rate Arbitrage Command Center ⚡
</pre>
</p>
<br/>

*A High-Performance, Asynchronous Python System That Scans 20 Cryptocurrency Exchanges In Real-Time To Identify Profitable Funding Rate Arbitrage Opportunities Across Perpetual Futures Markets.*

<br/>

[**Getting Started**](#-quick-start) •
[**Features**](#-features) •
[**Dashboard**](#%EF%B8%8F-web-dashboard) •
[**Configuration**](#%EF%B8%8F-configuration) •
[**Docker**](#-docker-deployment) •
[**Contributing**](#-contributing)

<br/>

---

</div>

<br/>

## 🎯 What is Funding Rate Arbitrage?  

Funding rates are periodic payments exchanged between long and short positions in perpetual futures markets. When there's a **significant difference** in funding rates between exchanges, you can:  

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│   📈 LONG on Exchange A (Low/Negative Rate) → RECEIVE Funding      │
│                          +                                         │
│   📉 SHORT on Exchange B (High/Positive Rate) → RECEIVE Funding    │
│                          =                                         │
│   💰 PROFIT from the Spread (Market Neutral Position)              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**ATHENA** automatically scans all 20 markets and alerts you when profitable spreads appear. 

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚀 Performance
- **Ultra-fast async fetching** with `aiohttp` + connection pooling
- **Parallel execution** — all 20 exchanges fetched via `asyncio.gather`
- **Per-exchange timeout** of 10s (slow exchanges don't block the cycle)
- **Connection pool** of 128 connections, 16 per host
- **DNS cache** with 10-minute TTL
- **HTTP keep-alive** connections reused across cycles
- **uvloop** integration for blazing speed on Linux
- **`orjson`** for 3-5x faster JSON serialization in dashboard

### 📊 Real-Time Dashboard
- Beautiful glassmorphism web UI with TailwindCSS
- Live opportunity table with search & filtering
- Interactive Chart.js bar graphs for top spreads
- UTC clock & funding countdown timer
- Exchange dominance analytics
- Pre-serialized JSON responses (zero-cost HTTP reads)

</td>
<td width="50%">

### 🔔 Smart Alerts
- **Telegram notifications** with rich Markdown formatting
- Hourly digest of top 10 opportunities
- Customizable spread thresholds (`MIN_SPREAD`)
- Multi-chat support (comma-separated `TELEGRAM_CHAT_IDS`)

### 📈 Analytics
- Annualized spread calculations (`spread × 3 × 365`)
- Exchange dominance tracking (best long/short sources)
- Opportunity count per cycle
- Top spread highlighted in real-time

</td>
</tr>
</table>

<br/>

## 🏦 Supported Exchanges

| # | Exchange | # | Exchange | # | Exchange | # | Exchange |
|:-:|----------|:-:|----------|:-:|----------|:-:|----------|
| 1 | Binance | 6 | MEXC | 11 | dYdX | 16 | Coinbase |
| 2 | Bybit | 7 | Huobi | 12 | Blofin | 17 | Hyperliquid |
| 3 | GateIO | 8 | BingX | 13 | Deribit | 18 | CoinEx |
| 4 | KuCoin | 9 | Kraken | 14 | HTX | 19 | BitUnix |
| 5 | Bitget | 10 | DeltaExchange | 15 | Crypto.com | 20 | Poloniex |

**20 Exchanges** • **3,000+ Trading Pairs** • **Real-Time Data**

<br/>

## 🖥️ Web Dashboard

The built-in **Command Center** provides a stunning real-time interface:  

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ⚡ ATHENA                                            🟢 System Online        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ ┌────────────────┐  │
│  │ TOP SPREAD  │ │OPPORTUNITIES│ │ EXCHANGE DOMINANCE  │ │  METADATA      │  │
│  │   0.4523%   │ │     47      │ │ Long:     Bybit     │ │ 20 Exch.       │  │
│  │  High Yield │ │   Active    │ │ Short:  Binance     │ │ 3000+ Pairs    │  │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ └────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │  #  │  PAIR      │  SPREAD   │  STRATEGY           │  LONG │ SHORT   │    │
│  ├─────┼────────────┼───────────┼─────────────────────┼───────┼─────────┤    │
│  │  1  │  XYZUSDT   │ +0.4523%  │  Bybit → Binance    │ -0.02%│ +0.43%  │    │
│  │  2  │  ABCUSDT   │ +0.3891%  │  DeltaEx → Bitget   │ -0.01%│ +0.38%  │    │
│  │  3  │  DEFUSDT   │ +0.2156%  │  KuCoin → MEXC      │ +0.05%│ +0.27%  │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- 🎨 Dark glassmorphism design with neon accents
- 📊 Live Chart.js bar graphs for top 5 spreads
- 🔍 Real-time search & filtering by symbol
- ⏱️ UTC clock & funding countdown timer (00:00/08:00/16:00)
- 📡 Live execution feed with animated log entries
- 📡 Activity feed with live execution logs

<br/>

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System.git
cd Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings
```

### Run

```bash
# Start the arbitrage engine
python main.py
```

🌐 **Dashboard:** Open [http://localhost:5000](http://localhost:5000) in your browser

<br/>

## ⚙️ Configuration

Create a `.env` file in the project root:  

```env
# ATHENA CONFIGURATION

# Minimum spread threshold (%) to trigger an opportunity
MIN_SPREAD=0.025

# Data fetch interval in seconds (0 = continuous)
FETCH_INTERVAL=0

# TELEGRAM ALERTS
# Get your bot token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Chat IDs to receive alerts (comma-separated for multiple)
TELEGRAM_CHAT_IDS=123456789,987654321

# Dashboard port (default: 5000)
WEB_PORT=5000
```

### Environment Variables

| Variable | Default | Description |
|:---------|:-------:|:------------|
| `MIN_SPREAD` | `0.025` | Minimum spread (%) to flag as opportunity |
| `FETCH_INTERVAL` | `0` | Seconds between cycles (`0` = no delay) |
| `TELEGRAM_BOT_TOKEN` | — | Telegram bot token from @BotFather |
| `TELEGRAM_CHAT_IDS` | — | Comma-separated chat IDs for alerts |
| `WEB_PORT` | `5000` | Flask dashboard port |

<br/>

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f athena

# Stop
docker compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t athena .

# Run container
docker run -d \
  --name athena-arb \
  --restart unless-stopped \
  -p 5000:5000 \
  --env-file .env \
  athena
```

**Docker Features:**
- 🔒 Read-only filesystem with tmpfs for `/tmp`
- 🏥 Built-in health check (`/api/data` endpoint)
- 📝 JSON log rotation (10MB × 3 files)
- 🔄 Auto-restart on failure

<br/>

## 📁 Project Structure

```
📦 Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System
├── 🚀 main.py              # Entry point — async loop, arbitrage calc, Rich CLI
├── 📡 fetcher.py           # 20 async exchange fetchers with connection pooling
├── 🌐 web_dashboard.py     # Flask dashboard + API (orjson, pre-serialized)
├── 🔔 notifier.py          # Telegram notification system
├── 📊 models.py            # Pydantic models (FundingRate, Opportunity)
├── 📋 requirements.txt     # Python dependencies
├── 🐳 Dockerfile           # Multi-stage Docker build
├── 🐳 docker-compose.yml   # Docker Compose config
├── 🔐 .env                 # Environment variables
└── 📄 LICENSE              # MIT License
```

<br/>

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|:--------:|:-------------|
| **Runtime** | ![Python](https://img.shields.io/badge/Python_3.9+-3776AB?style=flat-square&logo=python&logoColor=white) ![uvloop](https://img.shields.io/badge/uvloop-00ADD8?style=flat-square&logoColor=white) |
| **Async** | ![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=flat-square&logo=aiohttp&logoColor=white) ![asyncio](https://img.shields.io/badge/asyncio-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Web** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat-square&logo=tailwindcss&logoColor=white) |
| **Data** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) |
| **Speed** | ![orjson](https://img.shields.io/badge/orjson-FD4B5C?style=flat-square&logoColor=white) ![Rich](https://img.shields.io/badge/Rich-4B8BBE?style=flat-square&logoColor=white) |
| **Alerts** | ![Telegram](https://img.shields.io/badge/Telegram_Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white) |
| **Deploy** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) |

</div>

<br/>

## 📱 Telegram Alerts

ATHENA sends beautifully formatted alerts directly to your Telegram:  

```
⚡ ARB SIGNAL DETECTED ⚡
───────────────────
🕒 14:00 UTC
💎 Best Spread: +0.4523%
📊 Opportunities:  47

🏆 TOP 10 PER ROUND (8H)

🥇 XYZUSDT │ +0.4523%
   L: Bybit (-0.0234%)
   S: Binance (+0.4289%)

🥈 ABCUSDT │ +0.3891%
   L: DeltaExchange (-0.0156%)
   S: Bitget (+0.3735%)

🥉 DEFUSDT │ +0.2156%
   L: KuCoin (+0.0512%)
   S: MEXC (+0.2668%)

───────────────────
🖥️ Live Command Center
```

<br/>

## 🧮 How It Works

### Arbitrage Calculation

```python
# 1. Normalize symbols (remove -/_/, convert to uppercase)
# 2. Filter to USDT perpetual pairs only
# 3. Group by normalized symbol across all exchanges
# 4. For each symbol with 2+ exchanges:
#    - Find min rate (best long — receives funding)
#    - Find max rate (best short — receives funding)
#    - Spread = max_rate - min_rate
#    - If spread >= MIN_SPREAD → create Opportunity
# 5. Sort by spread descending
```

### Performance Optimizations

| Optimization | Impact |
|:-------------|:-------|
| `asyncio.gather` for parallel fetch | 20 exchanges in ~max(latency), not sum |
| Per-exchange timeout (10s) | Slow exchanges don't block the cycle |
| Connection pooling (128/16) | Reuse TCP connections across cycles |
| DNS caching (10min TTL) | Skip DNS lookup for repeated requests |
| HTTP keep-alive | Avoid TCP handshake overhead |
| `orjson` for JSON | 3-5x faster than stdlib `json` |
| Pre-serialized dashboard JSON | Zero-cost HTTP reads |
| Min/max instead of sort | O(n) vs O(n log n) for arbitrage calc |
| Instrument caching (CryptoCom, Poloniex) | Refresh every 30 min, not every cycle |

<br/>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 **Open** a Pull Request

### Ideas for Contribution
- [ ] Add more exchanges (OKX, Bitstamp, XT.com, etc.)
- [ ] Implement historical data tracking & storage
- [ ] Add automated trading execution
- [ ] Build mobile app interface
- [ ] Add webhook notifications (Discord, Slack)
- [ ] Implement backtesting engine

<br/>

## ⚠️ Disclaimer

> **This software is for educational and research purposes only.**
> 
> Cryptocurrency trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred from using this software. Always do your own research and never trade with money you cannot afford to lose. 

<br/>

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. 

<br/>

---

<div align="center">

**Built with 💜 by [Siddharthk17](https://github.com/Siddharthk17)**

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Siddharthk17-181717?style=for-the-badge&logo=github)](https://github.com/Siddharthk17)
[![Stars](https://img.shields.io/github/stars/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System?style=for-the-badge&logo=github&color=6366f1)](https://github.com/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System)

<br/>

*If you found this project helpful, please consider giving it a ⭐*

</div>
