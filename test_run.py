"""
立即測試腳本：不等排程，直接跑一次完整流程
執行方式：python test_run.py
"""
from fetchers.fomc import fetch_fomc_dates
from fetchers.earnings import fetch_earnings_dates
from fetchers.trump_news import fetch_trump_news
from notifier.formatter import format_weekly_report
from notifier.telegram import send_telegram_message


def main():
    print("🧪 測試模式：立即執行週報流程\n")

    print("1️⃣  抓取 FOMC 會議...")
    fomc = fetch_fomc_dates()
    print(f"   找到 {len(fomc)} 筆")

    print("2️⃣  抓取科技財報日...")
    earnings = fetch_earnings_dates()
    print(f"   找到 {len(earnings)} 筆")

    print("3️⃣  抓取川普政策要聞...")
    news = fetch_trump_news()
    print(f"   找到 {len(news)} 則新聞")

    print("\n4️⃣  組合訊息...")
    message = format_weekly_report(fomc, earnings, news)
    print("\n--- 預覽訊息 ---")
    print(message)
    print("--- 結束預覽 ---\n")

    send = input("是否發送到 Telegram？(y/N) ").strip().lower()
    if send == "y":
        send_telegram_message(message)
    else:
        print("✅ 測試完成，未發送")


if __name__ == "__main__":
    main()
