# Mr. Market Project Overview

## 📋 Summary
**Mr. Market ** is a lightweight, automated global financial market data aggregation platform. Its primary goal is to provide real-time, high-signal market snapshots in Markdown/HTML format, covering stocks, commodities, bonds, forex, news, and prediction markets.

The project leverages **Gemini Skills** and **Python-based Agents** to fetch data from multiple sources including TradingEconomics, Wallstreetcn (华尔街见闻), and Polymarket.

## 🏗️ Technical Architecture
- **Data Collection**: Python scripts located in `skills/*/scripts/` handle API/Web scraping.
- **Skill Layer**: Gemini Skills (`skills/*/SKILL.md`) define the orchestration and formatting logic.
- **Storage**: Real-time data is stored in JSON/Markdown files (refer to `idea/product-doc.md` for the planned structure).
- **Timezone**: Primary timezone is **UTC+8 (Beijing Time)**.

## 🛠️ Key Operations

### 1. Generating Market Dashboard
To generate the global market dashboard, use the `simple_quick-market-dashbord` skill.
- **Primary Method**: Run the scraper script:
  ```bash
  python3 ./skills/simple_quick-market-dashbord/scripts/fetch_market_data.py
  ```
- **Skill Usage**: Trigger by asking for "global market overview", "today's market status", or "market dashboard".

### 2. Web Service & Automation (Nginx)
The project is hosted as an **Agent-First** web service.
- **Web Root**: `/root/web-data/mr.market/web`
- **Nginx Config**: Located at `nginx/mr-market-agent.conf`.
- **Endpoint**: `/market-dashboard` returns the raw Markdown file (`web/market-dashboard.md`).

#### Automation (OpenClaw / Cron)
To keep the dashboard updated for other agents, schedule the following command to update the web file:
```bash
# Example Cron task (every 15 minutes)
*/15 * * * * claude -s simple_quick-market-dashbord > /root/web-data/mr.market/web/market-dashboard.md
```

### 3. Indicators Reference
For a mapping of common financial instruments to their source codes (e.g., US500, SHANGHAI), refer to:
`./skills/simple_quick-market-dashbord/references/indicators.md`

## 📏 Development & Interaction Rules
- **Precision**: All financial data **MUST** include a full date, time, and explicit timezone (UTC+8).
- **Attribution**: Every data point **MUST** be attributed to its source (e.g., TradingEconomics).
- **Formatting**: Dashboards follow a strict Markdown structure defined in `skills/simple_quick-market-dashbord/SKILL.md`.
- **Security**: Never expose API keys. Use provided scripts for data fetching to ensure robustness against upstream site changes.

## 📂 Directory Structure
- `skills/`: Gemini skill definitions, scripts, and evaluation data.
- `skills/simple_quick-market-dashbord/`: The core skill for market data.
- `skills/*-workspace/`: Temporary evaluation results (ignored by git).
