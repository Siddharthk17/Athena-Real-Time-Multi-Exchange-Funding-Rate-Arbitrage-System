<div align="center">

# ⚡ ATHENA

### Real-Time Multi-Exchange Funding Rate Arbitrage System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB? style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Async](https://img.shields.io/badge/Async-Powered-6366f1?style=for-the-badge&logo=fastapi&logoColor=white)](https://docs.python.org/3/library/asyncio.html)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Exchanges](https://img.shields.io/badge/Exchanges-13+-ef4444?style=for-the-badge&logo=bitcoin&logoColor=white)](#-supported-exchanges)

<br/>

<img src="https://img.shields.io/badge/⚡_Ultra_Low_Latency-~200ms-6366f1?style=flat-square" />
<img src="https://img.shields.io/badge/📡_Real--Time_Scanning-Active-10b981?style=flat-square" />
<img src="https://img.shields.io/badge/🤖_Telegram_Alerts-Enabled-06b6d4?style=flat-square" />

<br/><br/>

```
    █████╗ ████████╗██╗  ██╗███████╗███╗   ██╗ █████╗ 
   ██╔══██╗╚══██╔══╝██║  ██║██╔════╝████╗  ██║██╔══██╗
   ███████║   ██║   ███████║█████╗  ██╔██╗ ██║███████║
   ██╔══██║   ██║   ██╔══██║██╔══╝  ██║╚██╗██║██╔══██║
   ██║  ██║   ██║   ██║  ██║███████╗██║ ╚████║██║  ██║
   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                                       
   ⚡ Funding Rate Arbitrage Command Center ⚡
```

<br/>

*A high-performance, asynchronous Python system that scans 13+ cryptocurrency exchanges in real-time to identify profitable funding rate arbitrage opportunities across perpetual futures markets.*

<br/>

[**Getting Started**](#-quick-start) •
[**Features**](#-features) •
[**Dashboard**](#-web-dashboard) •
[**Configuration**](#%EF%B8%8F-configuration) •
[**Contributing**](#-contributing)

<br/>

---

</div>

<br/>

## 🎯 What is Funding Rate Arbitrage? 

Funding rates are periodic payments exchanged between long and short positions in perpetual futures markets. When there's a **significant difference** in funding rates between exchanges, you can: 

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   📈 LONG on Exchange A (Low/Negative Rate) → RECEIVE Funding      │
│                          +                                          │
│   📉 SHORT on Exchange B (High/Positive Rate) → RECEIVE Funding    │
│                          =                                          │
│   💰 PROFIT from the Spread (Market Neutral Position)              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**ATHENA** automatically scans all markets and alerts you when profitable spreads appear. 

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚀 **Performance**
- **Ultra-fast async fetching** with `aiohttp`
- **~200ms** update cycle across all exchanges
- **uvloop** integration for blazing speed on Unix
- Thread-safe, production-ready architecture

### 📊 **Real-Time Dashboard**
- Beautiful glassmorphism web UI
- Live opportunity table with filtering
- Interactive Chart. js visualizations
- Funding countdown timer
- Exchange dominance analytics

</td>
<td width="50%">

### 🔔 **Smart Alerts**
- **Telegram notifications** with rich formatting
- Hourly digest of top opportunities
- Customizable spread thresholds
- Multi-chat support

### 📈 **Analytics**
- Annualized spread calculations
- Exchange dominance tracking
- Historical opportunity logging
- Top long/short exchange detection

</td>
</tr>
</table>

<br/>

## 🏦 Supported Exchanges

<div align="center">

| Exchange | Status | Exchange | Status |
|: --------:|:------:|:--------:|: ------:|
| ![Binance](https://img.shields.io/badge/Binance-FCD535?style=flat-square&logo=binance&logoColor=black) | ✅ Live | ![OKX](https://img.shields.io/badge/OKX-000000?style=flat-square&logoColor=white) | ✅ Live |
| ![Bybit](https://img.shields.io/badge/Bybit-F7A600?style=flat-square&logoColor=white) | ✅ Live | ![KuCoin](https://img.shields.io/badge/KuCoin-23AF91?style=flat-square&logoColor=white) | ✅ Live |
| ![Bitget](https://img.shields.io/badge/Bitget-00CEA6?style=flat-square&logoColor=white) | ✅ Live | ![Gate.io](https://img.shields.io/badge/Gate. io-17E7B6?style=flat-square&logoColor=white) | ✅ Live |
| ![MEXC](https://img.shields.io/badge/MEXC-1972F5?style=flat-square&logoColor=white) | ✅ Live | ![Huobi](https://img.shields.io/badge/Huobi-1F5CFF?style=flat-square&logoColor=white) | ✅ Live |
| ![BingX](https://img.shields.io/badge/BingX-2952CC?style=flat-square&logoColor=white) | ✅ Live | ![Kraken](https://img.shields.io/badge/Kraken-5741D9?style=flat-square&logoColor=white) | ✅ Live |
| ![dYdX](https://img.shields.io/badge/dYdX-6966FF?style=flat-square&logoColor=white) | ✅ Live | ![BitMEX](https://img.shields.io/badge/BitMEX-D83E31?style=flat-square&logoColor=white) | ✅ Live |
| ![Phemex](https://img.shields.io/badge/Phemex-B89EFF?style=flat-square&logoColor=white) | ✅ Live | | |

**13 Exchanges** • **Hundreds of Trading Pairs** • **Real-Time Data**

</div>

<br/>

## 🖥️ Web Dashboard

The built-in **Command Center** provides a stunning real-time interface: 

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ⚡ ATHENA                                           🟢 System Online   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ ┌────────────┐ │
│  │ TOP SPREAD  │ │ OPPORTUNITIES│ │ EXCHANGE DOMINANCE  │ │  METADATA  │ │
│  │   0.4523%   │ │     47      │ │ Long:  Bybit         │ │ 13 Exch.    │ │
│  │  High Yield │ │   Active    │ │ Short: Binance      │ │ 892 Pairs  │ │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ └────────────┘ │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  #  │  PAIR      │  SPREAD   │  STRATEGY           │  LONG │ SHORT │ │
│  ├─────┼────────────┼───────────┼─────────────────────┼───────┼───────┤ │
│  │  1  │  XYZUSDT   │ +0.4523%  │  Bybit → Binance    │ -0.02%│ +0.43%│ │
│  │  2  │  ABCUSDT   │ +0.3891%  │  OKX → Bitget       │ -0.01%│ +0.38%│ │
│  │  3  │  DEFUSDT   │ +0.2156%  │  KuCoin → MEXC      │ +0.05%│ +0.27%│ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- 🎨 Dark glassmorphism design with neon accents
- 📊 Live Chart. js bar graphs for top spreads
- 🔍 Real-time search & filtering
- ⏱️ UTC clock & funding countdown timer
- 📡 Activity feed with live execution logs

<br/>

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System. git
cd Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example . env
# Edit . env with your settings
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
# ═══════════════════════════════════════════════════════════════
#                    ATHENA CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Minimum spread threshold (%) to trigger an opportunity
MIN_SPREAD=0.025

# Data fetch interval in seconds
FETCH_INTERVAL=0.0001

# ───────────────────── TELEGRAM ALERTS ─────────────────────────
# Get your bot token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Chat IDs to receive alerts (comma-separated for multiple)
TELEGRAM_CHAT_IDS=123456789,987654321
```

<br/>

## 📁 Project Structure

```
📦 Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System
├── 🚀 main.py              # Application entry point & orchestrator
├── 📡 fetcher.py           # Async exchange data fetchers (13 exchanges)
├── 🌐 web_dashboard.py     # Flask web UI & API endpoints
├── 🔔 notifier.py          # Telegram notification system
├── 📊 models.py            # Pydantic data models (FundingRate, Opportunity)
├── 📋 requirements.txt     # Python dependencies
├── 🔐 . env                 # Environment configuration
└── 📄 LICENSE              # MIT License
```

<br/>

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|:--------:|:-------------|
| **Runtime** | ![Python](https://img.shields.io/badge/Python_3.9+-3776AB?style=flat-square&logo=python&logoColor=white) ![uvloop](https://img.shields.io/badge/uvloop-00ADD8? style=flat-square&logoColor=white) |
| **Async** | ![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=flat-square&logo=aiohttp&logoColor=white) ![asyncio](https://img.shields.io/badge/asyncio-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Web** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) |
| **Data** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) ![Chart.js](https://img.shields.io/badge/Chart. js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) |
| **Alerts** | ![Telegram](https://img.shields.io/badge/Telegram_Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white) |
| **CLI** | ![Rich](https://img.shields.io/badge/Rich-4B8BBE?style=flat-square&logoColor=white) |

</div>

<br/>

## 📱 Telegram Alerts

ATHENA sends beautifully formatted alerts directly to your Telegram: 

```
⚡ ARB SIGNAL DETECTED ⚡
───────────────────
🕒 14:00 UTC
💎 Best Spread: +0.4523%
📊 Opportunities: 47

🏆 TOP 10 PER ROUND (8H)

🥇 XYZUSDT │ +0.4523%
   📈 Bybit (-0.0234%) → 📉 Binance (+0.4289%)

🥈 ABCUSDT │ +0.3891%
   📈 OKX (-0.0156%) → 📉 Bitget (+0.3735%)

🥉 DEFUSDT │ +0.2156%
   📈 KuCoin (+0.0512%) → 📉 MEXC (+0.2668%)
```

<br/>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 **Open** a Pull Request

### Ideas for Contribution
- [ ] Add more exchanges (Deribit, Coinbase, etc.)
- [ ] Implement historical data tracking
- [ ] Create Docker containerization
- [ ] Add automated trading execution
- [ ] Build mobile app interface

<br/>

## ⚠️ Disclaimer

> **This software is for educational and research purposes only. ** 
> 
> Cryptocurrency trading involves substantial risk of loss.  The authors are not responsible for any financial losses incurred from using this software.  Always do your own research and never trade with money you cannot afford to lose. 

<br/>

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

<br/>

---

<div align="center">

**Built with 💜 by [Siddharthk17](https://github.com/Siddharthk17)**

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Siddharthk17-181717?style=for-the-badge&logo=github)](https://github.com/Siddharthk17)
[![Stars](https://img.shields.io/github/stars/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System?style=for-the-badge&logo=github&color=6366f1)](https://github.com/Siddharthk17/Real-Time-Multi-Exchange-Funding-Rate-Arbitrage-System/stargazers)

<br/>

*If you found this project helpful, please consider giving it a ⭐*

</div>
