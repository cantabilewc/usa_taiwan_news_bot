"""
立即測試腳本：不等排程，直接跑一次完整流程
分兩則訊息發送：主報告 + AI 綜合心得
執行方式：python test_run.py
"""
from fetchers.fomc import fetch_fomc_dates
from fetchers.earnings import fetch_earnings_dates
from fetchers.trump_news import fetch_trump_news
from notifier.summarizer import summarize_all_news, generate_overall_insight
from notifier.formatter import format_main_report, format_insight_report, split_long_message
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

    print("4️⃣  生成 AI 逐則摘要...")
    news = summarize_all_news(news)
    print(f"   完成 {len(news)} 則摘要")

    print("5️⃣  生成 AI 綜合心得（約1000字）...")
    insight = generate_overall_insight(news)
    print(f"   完成，長度 {len(insight)} 字" if insight else "   略過（無內容或API未設定）")

    main_message = format_main_report(fomc, earnings, news)
    insight_message = format_insight_report(insight)

    print(f"\n--- 主報告預覽（長度 {len(main_message)} 字）---")
    print(main_message)
    print(f"\n--- AI心得預覽（長度 {len(insight_message)} 字）---")
    print(insight_message)
    print("--- 結束預覽 ---\n")

    send = input("是否發送到 Telegram？(y/N) ").strip().lower()
    if send == "y":
        for chunk in split_long_message(main_message):
            send_telegram_message(chunk)
        if insight_message:
            for chunk in split_long_message(insight_message):
                send_telegram_message(chunk)
    else:
        print("✅ 測試完成，未發送")


if __name__ == "__main__":
    main()
