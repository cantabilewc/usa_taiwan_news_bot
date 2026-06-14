"""
FOMC 會議日期抓取器
來源：美聯儲官網 + 內建年曆（作為 fallback）
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from config import LOOKAHEAD_DAYS


# 內建 2025–2026 FOMC 會議日期（備用，避免網路爬蟲失效）
FOMC_SCHEDULE = {
    2025: [
        "2025-01-28", "2025-01-29",
        "2025-03-18", "2025-03-19",
        "2025-05-06", "2025-05-07",
        "2025-06-17", "2025-06-18",
        "2025-07-29", "2025-07-30",
        "2025-09-16", "2025-09-17",
        "2025-10-28", "2025-10-29",
        "2025-12-09", "2025-12-10",
    ],
    2026: [
        "2026-01-27", "2026-01-28",
        "2026-03-17", "2026-03-18",
        "2026-04-28", "2026-04-29",
        "2026-06-17", "2026-06-18",
        "2026-07-28", "2026-07-29",
        "2026-09-15", "2026-09-16",
        "2026-10-27", "2026-10-28",
        "2026-12-15", "2026-12-16",
    ],
}


def fetch_fomc_dates() -> list[dict]:
    """
    取得未來兩週內的 FOMC 會議日期
    回傳格式：[{"date": "2025-06-17", "label": "FOMC 會議（Day 1）"}, ...]
    """
    today = datetime.today().date()
    two_weeks_later = today + timedelta(days=LOOKAHEAD_DAYS)

    events = []
    for year, dates in FOMC_SCHEDULE.items():
        for i in range(0, len(dates), 2):
            day1 = datetime.strptime(dates[i], "%Y-%m-%d").date()
            day2 = datetime.strptime(dates[i + 1], "%Y-%m-%d").date()

            if today <= day1 <= two_weeks_later:
                events.append({"date": dates[i], "label": "🏦 FOMC 會議 Day 1"})
            if today <= day2 <= two_weeks_later:
                events.append({"date": dates[i + 1], "label": "🏦 FOMC 會議 Day 2（決議公布）"})

    return sorted(events, key=lambda x: x["date"])
