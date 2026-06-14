"""
科技巨頭財報日抓取器
使用 yfinance 取得財報日期
"""
import yfinance as yf
from datetime import datetime, timedelta
from config import TECH_TICKERS, LOOKAHEAD_DAYS


def fetch_earnings_dates() -> list[dict]:
    """
    取得未來兩週內的財報日
    回傳格式：[{"date": "2025-07-29", "label": "📊 AAPL 財報日", "ticker": "AAPL"}, ...]
    """
    today = datetime.today().date()
    two_weeks_later = today + timedelta(days=LOOKAHEAD_DAYS)

    events = []

    for ticker_symbol in TECH_TICKERS:
        try:
            ticker = yf.Ticker(ticker_symbol)
            cal = ticker.calendar  # DataFrame or dict

            if cal is None:
                continue

            # yfinance 回傳格式可能是 dict 或 DataFrame
            if isinstance(cal, dict):
                earnings_date = cal.get("Earnings Date")
                if earnings_date:
                    # 可能是 list
                    if isinstance(earnings_date, list):
                        earnings_date = earnings_date[0]
                    date = earnings_date.date() if hasattr(earnings_date, 'date') else earnings_date
                    if today <= date <= two_weeks_later:
                        events.append({
                            "date": str(date),
                            "label": f"📊 {ticker_symbol} 財報日",
                            "ticker": ticker_symbol,
                        })
            else:
                # DataFrame 格式
                if "Earnings Date" in cal.columns:
                    for ed in cal["Earnings Date"]:
                        date = ed.date() if hasattr(ed, 'date') else ed
                        if today <= date <= two_weeks_later:
                            events.append({
                                "date": str(date),
                                "label": f"📊 {ticker_symbol} 財報日",
                                "ticker": ticker_symbol,
                            })
                            break  # 只取最近一次

        except Exception as e:
            print(f"⚠️ 無法取得 {ticker_symbol} 財報日期：{e}")
            continue

    return sorted(events, key=lambda x: x["date"])
