"""
單次執行腳本（給 Windows 工作排程器用）
每天/每週自動執行，FOMC 決議日會額外推播利率結果
"""
from fetchers.fomc import fetch_fomc_dates
from fetchers.earnings import fetch_earnings_dates
from fetchers.trump_news import fetch_trump_news
from fetchers.fed_decision import check_and_notify_fed_decision
from notifier.summarizer import summarize_all_news
from notifier.formatter import format_weekly_report
from notifier.telegram import send_telegram_message

# 主要週報
fomc = fetch_fomc_dates()
earnings = fetch_earnings_dates()
news = fetch_trump_news()
news = summarize_all_news(news)  # 加上 AI 中文摘要

message = format_weekly_report(fomc, earnings, news)
send_telegram_message(message)

# 若今天是 FOMC 決議日，額外推播利率結果
fed_msg = check_and_notify_fed_decision()
if fed_msg:
    send_telegram_message(fed_msg)
