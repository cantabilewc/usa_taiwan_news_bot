"""
設定檔：從環境變數讀取敏感資訊
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram 設定
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # BotFather 給的 token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 你的 chat id

# Anthropic API（用於 AI 新聞摘要）
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 要追蹤的科技巨頭股票（美股），依產業分類
US_STOCK_CATEGORIES = {
    "半導體/晶片設計": ["NVDA", "AMD", "AVGO", "MRVL", "INTC", "ARM", "MU"],
    "半導體設備/材料": ["ASML"],
    "雲端/AI軟體巨頭": ["MSFT", "GOOGL", "AMZN", "META", "ORCL"],
    "消費電子": ["AAPL"],
    "電動車/能源": ["TSLA"],
    "電腦硬體/伺服器": ["DELL"],
    "光通訊/AI基礎設施": ["LITE"],
    "航太/衛星/AI": ["SPCX"],
}
TECH_TICKERS = [t for tickers in US_STOCK_CATEGORIES.values() for t in tickers]

# 台股追蹤清單，依產業分類（用於股價分析與財報日提示）
TW_STOCK_CATEGORIES = {
    "晶圓代工": {"2330": "台積電"},
    "IC設計": {"2454": "聯發科"},
    "電子代工/AI伺服器": {"2317": "鴻海"},
    "電源/散熱": {"2308": "台達電"},
    "記憶體模組": {"8299": "群聯"},
    "連接器/線材(AI伺服器)": {"3665": "貿聯"},
    "封測": {"6147": "頎邦"},
}
TW_STOCKS = {code: name for group in TW_STOCK_CATEGORIES.values() for code, name in group.items()}

# 川普政策新聞最多抓幾則（減少篇幅，留空間給股價分析）
TRUMP_NEWS_MAX_ITEMS = 3

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
