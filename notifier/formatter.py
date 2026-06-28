"""
訊息格式化模組（純文字版，相容所有 Telegram 設定）
拆成兩則訊息發送，避免超過 Telegram 4096 字元上限
"""
from datetime import datetime, timedelta
from config import LOOKAHEAD_DAYS


def format_main_report(fomc_events: list, earnings_events: list, trump_news: list) -> str:
    """第一則訊息：FOMC、財報、新聞列表（不含 AI 心得）"""
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
            summary_text = news.get("ai_summary") or news.get("summary")
            if summary_text:
                lines.append(f"     💬 {summary_text}")
            if news.get("url"):
                lines.append(f"     🔗 {news['url']}")
    else:
        lines.append("  本週無相關要聞")

    lines.append("\n" + "=" * 30)
    lines.append("👉 AI 綜合心得將於下一則訊息發送")

    return "\n".join(lines)


def format_insight_report(overall_insight: str) -> str:
    """第二則訊息：AI 綜合心得（獨立發送，避免超字數限制）"""
    if not overall_insight:
        return ""

    lines = []
    lines.append("🧠 AI 綜合心得分析")
    lines.append("=" * 30)
    lines.append(overall_insight)
    lines.append("\n" + "=" * 30)
    lines.append("下次更新：明天凌晨00:00")

    return "\n".join(lines)


def split_long_message(text: str, limit: int = 4000) -> list[str]:
    """
    若單則訊息仍超過 Telegram 限制，依長度切成多段
    保留安全邊界（4000 而非 4096），避免邊界誤差
    """
    if len(text) <= limit:
        return [text]

    chunks = []
    while len(text) > limit:
        # 盡量在換行處切斷，避免斷在句子中間
        split_at = text.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")
    if text:
        chunks.append(text)
    return chunks


# 保留舊函式名稱以相容（若有其他地方呼叫到舊版 format_weekly_report）
def format_weekly_report(fomc_events: list, earnings_events: list, trump_news: list, overall_insight: str = "") -> str:
    """舊版相容函式：回傳合併內容（不建議使用，請改用 format_main_report + format_insight_report）"""
    main = format_main_report(fomc_events, earnings_events, trump_news)
    insight = format_insight_report(overall_insight)
    return main + "\n\n" + insight if insight else main
