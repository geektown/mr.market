# 📊 Mr. Market 

**Mr. Market** 是一个专为 AI Agent 设计的轻量级、自动化全球金融市场数据聚合平台。它通过定时任务抓取全球宏观数据、财经快讯和预测市场动态，并以原始 Markdown 格式通过 Web 服务实时分发。

## 🌟 核心特性

- **Agent-First 设计**：直接输出原始 Markdown，无冗余 HTML，极致节省其他 Agent 的 Token 消耗。
- **高时效与溯源**：所有数据均包含精确到秒的时间戳（UTC+8）和明确的数据源标注。
- **多源聚合**：
  - **TradingEconomics**：全球股票指数、大宗商品、外汇及债券收益率。
  - **华尔街见闻**：实时 7x24 财经快讯与深度头条。
  - **Polymarket**：基于预测市场的群体预期指标。
- **极简架构**：基于 Nginx 的静态文件分发，零性能损耗。

## 🚀 快速开始

### 1. 数据采集 (Skill 驱动)
直接运行 Python 采集脚本：
```bash
python3 ./skills/simple_quick-market-dashbord/scripts/fetch_market_data.py
```

### 2. 自动化调度 (OpenClaw / Cron)
配置定时任务将 Skill 输出重定向至 Web 目录：
```bash
*/15 * * * * claude -s simple_quick-market-dashbord > ./web/market-dashboard.md
```

### 3. Web 访问
配置 Nginx 托管 `./web` 目录，通过以下 Endpoint 获取数据：
- **GET** `/market-dashboard` -> 返回最新的 Markdown 数据。

## 📂 目录结构

- `skills/`: 包含核心采集脚本和 Gemini Skill 定义。
- `web/`: 存放实时生成的 Markdown 看板文件。
- `nginx/`: Nginx 配置文件备份。

---
**⚠️ 免责声明**：本项目提供的数据仅供参考，不构成任何投资建议。金融市场风险巨大，请务必核实官方原始信息。
