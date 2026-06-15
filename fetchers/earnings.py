"""
科技巨頭財報日抓取器
台股：靜態年曆（依歷史規律預估）+ 提示自行確認
美股：yfinance 動態抓取
"""
import yfinance as yf
from datetime import datetime, timedelta
from config import TECH_TICKERS, LOOKAHEAD_DAYS

# ──────────────────────────────────────────
# 台股法說會靜態年曆（預估日期，請留意官方公告）
# 法說會通常在財報截止日（8/14）前後舉行
# 來源：各公司歷史規律推估
# ──────────────────────────────────────────
TW_EARNINGS_SCHEDULE = [
    # Q2 2026 法說會（預估）
    {"date": "2026-07-16", "label": "📊 台積電 (2330) Q2 法說會 ⚠️預估"},
    {"date": "2026-07-29", "label": "📊 聯發科 (2454) Q2 法說會 ⚠️預估"},
    {"date": "2026-07-30", "label": "📊 群聯 (8299) Q2 法說會 ⚠️預估"},
    {"date": "2026-08-05", "label": "📊 台達電 (2308) Q2 法說會 ⚠️預估"},
    {"date": "2026-08-06", "label": "📊 鴻海 (2317) Q2 財報 ⚠️預估"},
    {"date": "2026-08-07", "label": "📊 貿聯 (3665) Q2 法說會 ⚠️預估"},
    {"date": "2026-08-10", "label": "📊 景碩 (3189) Q2 法說會 ⚠️預估"},
    {"date": "2026-08-11", "label": "📊 健策 (3653) Q2 法說會 ⚠️預估"},
    {"date": "2026-08-12", "label": "📊 頎邦 (6147) Q2 法說會 ⚠️預估"},

    # Q3 2026 法說會（預估，10~11月）
    {"date": "2026-10-15", "label": "📊 台積電 (2330) Q3 法說會 ⚠️預估"},
    {"date": "2026-10-28", "label": "📊 聯發科 (2454) Q3 法說會 ⚠️預估"},
    {"date": "2026-10-29", "label": "📊 群聯 (8299) Q3 法說會 ⚠️預估"},
    {"date": "2026-11-04", "label": "📊 台達電 (2308) Q3 法說會 ⚠️預估"},
    {"date": "2026-11-05", "label": "📊 鴻海 (2317) Q3 財報 ⚠️預估"},
    {"date": "2026-11-06", "label": "📊 貿聯 (3665) Q3 法說會 ⚠️預估"},
    {"date": "2026-11-09", "label": "📊 景碩 (3189) Q3 法說會 ⚠️預估"},
    {"date": "2026-11-10", "label": "📊 健策 (3653) Q3 法說會 ⚠️預估"},
    {"date": "2026-11-11", "label": "📊 頎邦 (6147) Q3 法說會 ⚠️預估"},
]


def fetch_tw_earnings_dates() -> list[dict]:
    """從靜態年曆篩出未來 LOOKAHEAD_DAYS 天內的台股法說會"""
    today = datetime.today().date()
    end_date = today + timedelta(days=LOOKAHEAD_DAYS)
    events = []
    for e in TW_EARNINGS_SCHEDULE:
        d = datetime.strptime(e["date"], "%Y-%m-%d").date()
        if today <= d <= end_date:
            events.append({"date": e["date"], "label": e["label"]})
    return events


def fetch_us_earnings_dates() -> list[dict]:
    """用 yfinance 動態抓美股財報日"""
    today = datetime.today().date()
    end_date = today + timedelta(days=LOOKAHEAD_DAYS)
    events = []

    for ticker_symbol in TECH_TICKERS:
        try:
            ticker = yf.Ticker(ticker_symbol)
            cal = ticker.calendar
            if cal is None:
                continue

            if isinstance(cal, dict):
                earnings_date = cal.get("Earnings Date")
                if earnings_date:
                    if isinstance(earnings_date, list):
                        earnings_date = earnings_date[0]
                    date = earnings_date.date() if hasattr(earnings_date, 'date') else earnings_date
                    if today <= date <= end_date:
                        events.append({"date": str(date), "label": f"📊 {ticker_symbol} 財報日"})
            else:
                if "Earnings Date" in cal.columns:
                    for ed in cal["Earnings Date"]:
                        date = ed.date() if hasattr(ed, 'date') else ed
                        if today <= date <= end_date:
                            events.append({"date": str(date), "label": f"📊 {ticker_symbol} 財報日"})
                            break
        except Exception as e:
            print(f"⚠️ 無法取得 {ticker_symbol} 財報日期：{e}")
            continue

    return events


def fetch_earnings_dates() -> list[dict]:
    """合併台股 + 美股財報日"""
    tw = fetch_tw_earnings_dates()
    us = fetch_us_earnings_dates()
    return sorted(tw + us, key=lambda x: x["date"])