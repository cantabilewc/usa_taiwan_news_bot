"""
排程模組：使用 APScheduler 在每週日晚上觸發推播
"""
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import SCHEDULE_DAY, SCHEDULE_HOUR, SCHEDULE_MINUTE
from fetchers.fomc import fetch_fomc_dates
from fetchers.earnings import fetch_earnings_dates
from fetchers.trump_news import fetch_trump_news
from notifier.summarizer import summarize_all_news
from notifier.formatter import format_weekly_report
from notifier.telegram import send_telegram_message


def run_weekly_job():
    """每週執行的主任務"""
    print("⏰ 開始執行週報任務...")

    fomc_events = fetch_fomc_dates()
    earnings_events = fetch_earnings_dates()
    trump_news = fetch_trump_news()

    print("🤖 正在生成 AI 摘要...")
    trump_news = summarize_all_news(trump_news)

    message = format_weekly_report(fomc_events, earnings_events, trump_news)
    send_telegram_message(message)

    print("✅ 週報已發送完畢！")


def start_scheduler():
    """啟動排程器"""
    scheduler = BlockingScheduler(timezone="Asia/Taipei")

    trigger = CronTrigger(
        day_of_week=SCHEDULE_DAY,
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        timezone="Asia/Taipei"
    )

    scheduler.add_job(run_weekly_job, trigger, id="weekly_market_report")

    print(f"📅 排程已設定：每週{SCHEDULE_DAY} {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} (台北時間)")
    print("💡 提示：若要立即測試，請執行 python test_run.py")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 排程器已停止")
