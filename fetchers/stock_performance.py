"""
台美股最近股價表現抓取器（依產業分類）
計算過去 7 天與過去 30 天的漲跌幅，給 AI 心得分析使用
"""
import yfinance as yf
from config import US_STOCK_CATEGORIES, TW_STOCK_CATEGORIES


def _calc_change(ticker_symbol: str) -> dict | None:
    """抓取單一股票過去 30 天的歷史股價，計算 7天/30天漲跌幅"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1mo")

        if hist.empty or len(hist) < 2:
            return None

        latest_price = hist["Close"].iloc[-1]
        price_7d_ago = hist["Close"].iloc[-6] if len(hist) >= 6 else hist["Close"].iloc[0]
        price_30d_ago = hist["Close"].iloc[0]

        change_7d = ((latest_price - price_7d_ago) / price_7d_ago) * 100
        change_30d = ((latest_price - price_30d_ago) / price_30d_ago) * 100

        return {
            "latest_price": round(float(latest_price), 2),
            "change_7d": round(float(change_7d), 2),
            "change_30d": round(float(change_30d), 2),
        }
    except Exception:
        return None  # 靜默失敗，讓上層決定是否嘗試 .TWO 後綴


def fetch_us_stock_performance() -> dict:
    """
    依分類抓美股股價表現
    回傳格式：{"半導體/晶片設計": [{"name": "NVDA", ...}, ...], ...}
    """
    results = {}
    for category, tickers in US_STOCK_CATEGORIES.items():
        category_results = []
        for symbol in tickers:
            data = _calc_change(symbol)
            if data:
                data["name"] = symbol
                category_results.append(data)
        if category_results:
            results[category] = category_results
    return results


def fetch_tw_stock_performance() -> dict:
    """
    依分類抓台股股價表現
    自動嘗試 .TW（上市）→ .TWO（上櫃），相容兩種掛牌類型
    回傳格式：{"晶圓代工": [{"name": "台積電", "ticker": "2330", ...}], ...}
    """
    results = {}
    for category, stocks in TW_STOCK_CATEGORIES.items():
        category_results = []
        for code, name in stocks.items():
            data = _calc_change(f"{code}.TW")
            if data is None:
                data = _calc_change(f"{code}.TWO")  # 上市抓不到，改試上櫃
            if data:
                data["name"] = name
                data["ticker"] = code
                category_results.append(data)
            else:
                print(f"⚠️ {name}({code}) 上市/上櫃皆抓取失敗，略過")
        if category_results:
            results[category] = category_results
    return results


def fetch_all_stock_performance() -> dict:
    """回傳台美股完整分類表現資料"""
    return {
        "us": fetch_us_stock_performance(),
        "tw": fetch_tw_stock_performance(),
    }
