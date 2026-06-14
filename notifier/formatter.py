"""
訊息格式化模組（純文字版，相容所有 Telegram 設定）
"""
from datetime import datetime, timedelta
from config import LOOKAHEAD_DAYS


def format_weekly_report(fomc_events: list, earnings_events: list, trump_news: list) -> str:
    today = datetime.today()
    two_weeks_later = today + timedelta(days=LOOKAHEAD_DAYS)

    lines = []
    lines.append("📰 每季市場大事週報（未來90天）")
    lines.append(f"📅 {today.strftime('%Y/%m/%d')} ~ {two_weeks_later.strftime('%m/%d')}")
    lines.append("=" * 30)

    # FOMC
    lines.append("\n🏦 FOMC 聯準會會議")
    if fomc_events:
        for e in fomc_events:
            lines.append(f"  • {e['date']}  {e['label']}")
    else:
        lines.append("  未來兩週無 FOMC 會議")

    # 財報
    lines.append("\n📊 科技巨頭財報日")
    if earnings_events:
        for e in earnings_events:
            lines.append(f"  • {e['date']}  {e['label']}")
    else:
        lines.append("  未來兩週無追蹤標的財報")

    # 川普要聞
    lines.append("\n🇺🇸 川普政策近期要聞")
    if trump_news:
        for i, news in enumerate(trump_news, 1):
            date_prefix = f"[{news['date']}] " if news["date"] else ""
            lines.append(f"  {i}. {date_prefix}{news['title']}")
            if news.get("url"):
                lines.append(f"     {news['url']}")
    else:
        lines.append("  本週無相關要聞")

    lines.append("\n" + "=" * 30)
    lines.append("下次更新：明天凌晨00:00")

    return "\n".join(lines)
