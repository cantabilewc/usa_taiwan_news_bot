# 📰 Market Weekly Alert

每週日晚上自動推播台美股大事到 Telegram。

## 功能

- 🏦 未來兩週 FOMC 聯準會會議日期
- 📊 科技巨頭財報日（AAPL、MSFT、GOOGL、AMZN、META、NVDA、TSLA）
- 🇺🇸 川普政策相關要聞（RSS 即時抓取）

## 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 Telegram Bot
```bash
cp .env.example .env
# 編輯 .env，填入 TELEGRAM_TOKEN 和 TELEGRAM_CHAT_ID
```

**取得 TELEGRAM_TOKEN：**
- 在 Telegram 找 `@BotFather` → `/newbot` → 複製 token

**取得 TELEGRAM_CHAT_ID：**
- 對你的 bot 發送任意訊息
- 瀏覽 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
- 找 `result[0].message.chat.id`

### 3. 立即測試
```bash
python test_run.py
```

### 4. 啟動排程（每週日 20:00 台北時間自動發送）
```bash
python main.py
```

## 自訂設定

編輯 `config.py`：

```python
TECH_TICKERS = ["AAPL", "MSFT", ...]  # 追蹤的股票
SCHEDULE_HOUR = 20                      # 發送時間（24h）
TRUMP_KEYWORDS = ["Trump", "tariff"]   # 關鍵字過濾
```

## 長期運行建議

| 方式 | 說明 |
|---|---|
| `nohup python main.py &` | Linux 背景執行 |
| `systemd service` | Linux 系統服務（重開機自啟） |
| `cron` + 單次腳本 | 不用常駐，更輕量 |
| Raspberry Pi | 家用低耗電常駐 |

## 專案結構

```
market-weekly-alert/
├── main.py              # 入口
├── scheduler.py         # APScheduler 排程
├── config.py            # 設定
├── test_run.py          # 立即測試
├── fetchers/
│   ├── fomc.py          # FOMC 日期
│   ├── earnings.py      # 財報日（yfinance）
│   └── trump_news.py    # 川普要聞（RSS）
├── notifier/
│   ├── telegram.py      # Telegram 發送
│   └── formatter.py     # 訊息格式化
├── requirements.txt
└── .env.example
```
