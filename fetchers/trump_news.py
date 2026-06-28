"""
川普政策要聞抓取器
透過 RSS Feed + 關鍵字過濾，取得近期相關新聞
"""
import feedparser
from datetime import datetime, timedelta, timezone
from config import RSS_FEEDS, TRUMP_KEYWORDS, TRUMP_NEWS_MAX_ITEMS


def fetch_trump_news(max_items: int = None) -> list[dict]:
    """
    從 RSS 抓取川普相關重要新聞（過去 7 天 + 未來預告）
    回傳格式：[{"date": "2025-06-15", "title": "...", "url": "..."}, ...]
    """
    if max_items is None:
        max_items = TRUMP_NEWS_MAX_ITEMS
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    results = []
    seen_titles = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published_parsed")

                # 時間過濾
                if published:
                    pub_dt = datetime(*published[:6], tzinfo=timezone.utc)
                    if pub_dt < one_week_ago:
                        continue

                # 關鍵字過濾
                combined_text = f"{title} {summary}".lower()
                matched = any(kw.lower() in combined_text for kw in TRUMP_KEYWORDS)

                if matched and title not in seen_titles:
                    seen_titles.add(title)
                    date_str = ""
                    if published:
                        date_str = f"{published[0]}-{published[1]:02d}-{published[2]:02d}"

                    # 清理摘要：去除 HTML 標籤，截斷長度
                    import re
                    clean_summary = re.sub(r"<[^>]+>", "", summary).strip()
                    if len(clean_summary) > 150:
                        clean_summary = clean_summary[:150] + "..."

                    results.append({
                        "date": date_str,
                        "title": title[:80] + ("..." if len(title) > 80 else ""),
                        "summary": clean_summary,
                        "url": link,
                    })

        except Exception as e:
            print(f"⚠️ RSS 抓取失敗 ({feed_url})：{e}")
            continue

    # 按日期排序，只取最新 max_items 則
    results.sort(key=lambda x: x["date"], reverse=True)
    return results[:max_items]
