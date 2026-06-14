"""
市場週報通知機器人
每週日晚上自動抓取未來兩週重要事件並推播至 Telegram
"""
from scheduler import start_scheduler

if __name__ == "__main__":
    print("🚀 Market Weekly Alert Bot 啟動中...")
    start_scheduler()
