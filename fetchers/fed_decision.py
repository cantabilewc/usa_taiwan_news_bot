"""
Fed 利率決議抓取器
在 FOMC 會議結束當天（美東時間下午2點後）自動抓取聲明摘要
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date


# FOMC 決議公布日（第二天，美東 14:00）與對應 URL 日期碼
FOMC_DECISION_DATES = {
    "2026-01-28": "20260128",
    "2026-03-18": "20260318",
    "2026-04-29": "20260429",
    "2026-06-17": "20260617",  # 本次會議
    "2026-07-29": "20260729",
    "2026-09-16": "20260916",
    "2026-10-28": "20261028",
    "2026-12-16": "20261216",
}


def fetch_fed_decision(target_date: str = None) -> dict | None:
    """
    抓取指定日期的 Fed 利率決議聲明
    target_date: "YYYY-MM-DD" 格式，預設為今天
    回傳: {"rate": "3.50%~3.75%", "action": "維持不變", "summary": "..."}
    """
    if target_date is None:
        target_date = date.today().strftime("%Y-%m-%d")

    date_code = FOMC_DECISION_DATES.get(target_date)
    if not date_code:
        return None  # 今天不是 FOMC 決議日

    url = f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{date_code}a.htm"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # 抓主要內容段落
        content_div = soup.find("div", class_="col-xs-12 col-sm-8 col-md-8")
        if not content_div:
            content_div = soup.find("div", attrs={"id": "article"}) or soup.find("article")

        paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")
        full_text = " ".join(p.get_text(strip=True) for p in paragraphs[:6])

        # 判斷升降息
        action = "維持不變 ✅"
        if "lower" in full_text.lower() or "decrease" in full_text.lower() or "cut" in full_text.lower():
            action = "降息 📉"
        elif "raise" in full_text.lower() or "increase" in full_text.lower() or "hike" in full_text.lower():
            action = "升息 📈"

        # 抓利率數字
        import re
        rate_match = re.search(r"(\d+[\-–]\d+/\d+|\d+\s*to\s*\d+[\-–]\d+/\d+|\d+\.?\d*\s*to\s*\d+\.?\d*)\s*percent", full_text)
        rate_str = rate_match.group(0) if rate_match else "詳見聲明"

        # 取摘要（前兩段）
        summary = " ".join(p.get_text(strip=True) for p in paragraphs[:2])
        if len(summary) > 200:
            summary = summary[:200] + "..."

        return {
            "action": action,
            "rate": rate_str,
            "summary": summary,
            "url": url,
            "date": target_date,
        }

    except Exception as e:
        print(f"⚠️ 無法抓取 Fed 決議：{e}")
        return None


def check_and_notify_fed_decision() -> str | None:
    """
    檢查今天是否有 FOMC 決議，有的話回傳通知訊息
    """
    result = fetch_fed_decision()
    if not result:
        return None

    msg = (
        f"\n🚨 Fed 最新利率決議\n"
        f"{'=' * 30}\n"
        f"決定：{result['action']}\n"
        f"利率：{result['rate']}\n"
        f"摘要：{result['summary']}\n"
        f"完整聲明：{result['url']}"
    )
    return msg
