"""
單次執行腳本（給 Windows 工作排程器用）
分兩則訊息發送：主報告 + AI 綜合心得（含股價分析）
"""
from fetchers.fomc import fetch_fomc_dates
from fetchers.earnings import fetch_earnings_dates
from fetchers.trump_news import fetch_trump_news
from fetchers.stock_performance import fetch_all_stock_performance
from fetchers.fed_decision import check_and_notify_fed_decision
from notifier.summarizer import summarize_all_news, generate_overall_insight
from notifier.formatter import format_main_report, format_insight_report, split_long_message
from notifier.telegram import send_telegram_message

# 資料抓取
fomc = fetch_fomc_dates()
earnings = fetch_earnings_dates()
news = fetch_trump_news()
stock_perf = fetch_all_stock_performance()
news = summarize_all_news(news)
insight = generate_overall_insight(news, stock_performance=stock_perf)

# 第一則：主報告
main_message = format_main_report(fomc, earnings, news)
for chunk in split_long_message(main_message):
    send_telegram_message(chunk)

# 第二則：AI 綜合心得（股價分析為主）
insight_message = format_insight_report(insight)
if insight_message:
    for chunk in split_long_message(insight_message):
        send_telegram_message(chunk)

# FOMC 決議日額外推播
fed_msg = check_and_notify_fed_decision()
if fed_msg:
    send_telegram_message(fed_msg)
