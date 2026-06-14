"""
設定檔：從環境變數讀取敏感資訊
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram 設定
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # BotFather 給的 token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 你的 chat id

# 要追蹤的科技巨頭股票（美股）
TECH_TICKERS = ["LITE", "INTC", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "MU", "ORCL", "AVGO", "MRVL", "SPCX" , "ASML", "DELL", "AMD", "ARM"]

# 台股追蹤清單（用於提示，財報日以公司公告為準）
TW_STOCKS = ["2330", "2454", "2317", "2308", "8299", "3665", "6147"]  # 台積電、聯發科、鴻海

# RSS 新聞來源（川普 / 美國政策）
RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/politicsNews",
    "https://rss.politico.com/politics-news.xml",
    "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
]

# 關鍵字過濾（用於篩選川普相關新聞）
TRUMP_KEYWORDS = ["Trump", "川普", "tariff", "關稅", "White House", "executive order", "White House"]

# 往前看幾天（週報涵蓋範圍）
LOOKAHEAD_DAYS = 90

# 排程設定：每週日幾點發送（24h 制）
SCHEDULE_DAY = "sunday"
SCHEDULE_HOUR = 20   # 晚上 8 點
SCHEDULE_MINUTE = 0
