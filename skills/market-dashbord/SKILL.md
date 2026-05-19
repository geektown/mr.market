---
name: market-dashbord
description: Use this skill whenever the user asks for a global market dashboard, market overview, today's market status, or specific data from TradingEconomics, Wallstreetcn (华尔街见闻), or Polymarket. It provides a real-time, lightweight market summary formatted in Markdown, covering stocks, commodities, bonds, forex, news, and prediction markets. **CRITICAL: All data points and news items MUST include a date, time, explicit timezone, and the DATA SOURCE name.**
---

# market-dashbord

A skill to fetch, aggregate, and display global market status with precise timestamps and source attribution.

## Operational Workflow

### 1. Data Collection (Robust & High-Signal)
Use the bundled Python script for fast and reliable data collection. The script is designed for maximum robustness:
- **Scraping Strategy**: Uses `curl_cffi` with Chrome impersonation to bypass TradingEconomics anti-scraping measures.
- **Fallback Mechanism**: Automatically falls back to the `Yahoo Finance` (yfinance) for critical market indicators (S&P 500, Nasdaq, Gold, Oil, etc.) if TradingEconomics fails.
- **News & Predictions**: Fetches live news from Wallstreetcn and prediction data from Polymarket with enhanced timeouts.
- **Command**: `python3 ./skills/market-dashbord/scripts/fetch_market_data.py`
- **Output**: A JSON object containing `report_generated_at`, `stocks`, `commodities`, `currencies`, `bonds`, `wscn` (news), and `poly` (predictions). Each item includes a `source` field identifying if it came from TradingEconomics or YahooFinance (Fallback).

### 2. Attribution & Precision
- **Source Labeling**: You MUST clearly label the source for each section or data point (e.g., "Source: TradingEconomics").
- **Time & Date**: Every section starts with its specific update time in **UTC+8 (Beijing Time)**.
- **Backwards Compatibility**: If manual `web_fetch` is used, ensure the source name is correctly identified from the URL domain.

### 3. Save file
1. First, when the markdown file is generated, Move the old file to `~/web-data/mr.market/web/market-dashboard_${this_file_created_datetime}.md` to backup.
2. Second, save new generated file to `~/web-data/mr.market/web/market-dashboard.md`

## Output Structure

The output must be a high-signal Markdown dashboard. ALWAYS use this exact structure:

# 📊 Mr.Market 全球市场数据概览
*系统生成时间: YYYY-MM-DD HH:MM:SS (UTC+8)*

## 1. 🌍 宏观市场 (TradingEconomics)

### 📈 股票指数
| 指数 | 最新价 | 涨跌幅 | 更新时间 (UTC+8) | 数据源 |
| :--- | :--- | :--- | :--- | :--- |
| **标普 500** | [Price] | [Change%] | [Time] | TradingEconomics |
| **纳斯达克 100** | [Price] | [Change%] | [Time] | TradingEconomics |
| **上证综指** | [Price] | [Change%] | [Time] | TradingEconomics |
| **恒生指数** | [Price] | [Change%] | [Time] | TradingEconomics |

### 🛢️ 大宗商品 & 债券
| 资产 | 最新价 | 涨跌幅 | 更新时间 (UTC+8) | 数据源 |
| :--- | :--- | :--- | :--- | :--- |
| **现货黄金** | [Price] | [Change%] | [Time] | TradingEconomics |
| **WTI 原油** | [Price] | [Change%] | [Time] | TradingEconomics |
| **10年期美债** | [Yield] | [Change%] | [Time] | TradingEconomics |

### 💱 外汇市场
| 货币对 | 最新价 | 涨跌幅 | 更新时间 (UTC+8) | 数据源 |
| :--- | :--- | :--- | :--- | :--- |
| **美元指数** | [Price] | [Change%] | [Time] | TradingEconomics |
| **离岸人民币** | [Price] | [Change%] | [Time] | TradingEconomics |

## 2. 🗞️ 财经要闻 (华尔街见闻)
- 🔴 **[突发标题]** (链接) - *YYYY-MM-DD HH:MM:SS (UTC+8)* [来源: 华尔街见闻]
- 🔹 **[快讯标题]** (链接) - *YYYY-MM-DD HH:MM:SS (UTC+8)* [来源: 华尔街见闻]
- ... (展示最近 10 条快讯)

## 3. 🔮 预测市场 (Polymarket)
- 🗳️ **[事件名称]**: **[Outcomes]** (24h 交易量: $[Vol], 来源: Polymarket)
- ... (展示 5 个热门市场)

---
**⚠️ 注意：** 金融市场实时变动，以上数据均来自第三方公开渠道（TradingEconomics, 华尔街见闻, Polymarket），仅供参考，不构成投资建议。
