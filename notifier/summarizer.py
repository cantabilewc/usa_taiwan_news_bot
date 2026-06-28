"""
AI 新聞摘要模組
使用 Anthropic Claude API 將英文新聞摘要轉成簡潔中文重點
"""
import requests
from config import ANTHROPIC_API_KEY

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"  # 用 Haiku：快速、便宜，適合簡單摘要任務


def summarize_news(title: str, raw_summary: str) -> str:
    """
    把單則新聞標題 + 原始摘要，轉成一句中文重點
    若 API 呼叫失敗，回傳原始摘要（fallback，不讓程式中斷）
    """
    if not ANTHROPIC_API_KEY:
        return raw_summary  # 沒設定 API key，直接退回原文

    prompt = (
        f"以下是一則新聞的標題與摘要，請用繁體中文寫出一句話重點摘要（不超過50字），"
        f"只回傳摘要本身，不要加任何前言或標籤：\n\n"
        f"標題：{title}\n"
        f"摘要：{raw_summary}"
    )

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 150,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        result = "".join(text_blocks).strip()
        return result if result else raw_summary
    except Exception as e:
        print(f"⚠️ AI 摘要失敗，使用原始摘要：{e}")
        return raw_summary


def summarize_all_news(news_list: list[dict]) -> list[dict]:
    """
    對整批新聞逐一生成 AI 摘要，回傳新的 list（加上 ai_summary 欄位）
    """
    results = []
    for news in news_list:
        ai_summary = summarize_news(news.get("title", ""), news.get("summary", ""))
        news_copy = dict(news)
        news_copy["ai_summary"] = ai_summary
        results.append(news_copy)
    return results


def generate_overall_insight(news_list: list[dict], stock_performance: dict = None) -> str:
    """
    結合川普政策新聞 + 台美股近期股價表現，生成約 1000 字綜合心得分析
    內容包含股市影響層級評估（高/中/低）與重點產業影響
    若 API 未設定，回傳空字串（formatter 會自動跳過該區塊）

    stock_performance 格式：{"us": [...], "tw": [...]}（來自 fetch_all_stock_performance）
    """
    if not ANTHROPIC_API_KEY:
        return ""

    # 川普新聞部分（精簡，只當作背景脈絡，不要佔太多篇幅）
    news_section = "（本週無相關要聞）"
    if news_list:
        news_section = "\n\n".join(
            f"標題：{n.get('title', '')}\n摘要：{n.get('summary', '') or n.get('ai_summary', '')}"
            for n in news_list
        )

    # 股價表現部分（依分類呈現）
    stock_section = "（無股價資料）"
    if stock_performance:
        lines = []
        us_categories = stock_performance.get("us", {})
        tw_categories = stock_performance.get("tw", {})

        if us_categories:
            lines.append("【美股】")
            for category, stocks in us_categories.items():
                lines.append(f"◆ {category}")
                for s in stocks:
                    lines.append(
                        f"  {s['name']}：現價 {s['latest_price']}，"
                        f"近7日 {s['change_7d']:+.2f}%，近30日 {s['change_30d']:+.2f}%"
                    )
        if tw_categories:
            lines.append("【台股】")
            for category, stocks in tw_categories.items():
                lines.append(f"◆ {category}")
                for s in stocks:
                    lines.append(
                        f"  {s['name']}({s['ticker']})：現價 {s['latest_price']}，"
                        f"近7日 {s['change_7d']:+.2f}%，近30日 {s['change_30d']:+.2f}%"
                    )
        if lines:
            stock_section = "\n".join(lines)

    prompt = (
        "你是一位財經觀察者，請根據以下兩組資料，寫一段約 1200 字的繁體中文綜合心得：\n"
        "（A）過去一週與川普政策相關的新聞（僅供背景參考）\n"
        "（B）台美股科技權值股近期股價表現，已依產業分類整理（7日/30日漲跌幅）\n\n"
        "請將大部分篇幅放在【股價表現分析】上，依產業分類逐一點評，川普政策新聞僅作為背景脈絡簡要提及即可。"
        "內容須包含：\n"
        "1. 依產業分類，點出各類別中表現最強與最弱的標的，並說明可能原因\n"
        "2. 台股與美股同類產業（如台積電vs.美系半導體）的連動性觀察\n"
        "3. 川普政策動向對這些股價走勢可能的關聯（簡要說明即可，1-2句帶過）\n"
        "4. 對台美股市未來走向的影響評估，標示「影響層級」（高／中／低）並說明理由\n"
        "5. 最值得關注的1-2個產業類別或個股，並說明原因\n"
        "請直接輸出心得內容，不要加標題或前言：\n\n"
        f"【A. 川普政策新聞】\n{news_section}\n\n"
        f"【B. 台美股股價表現（依產業分類）】\n{stock_section}"
    )

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()
        text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        result = "".join(text_blocks).strip()
        return result
    except Exception as e:
        print(f"⚠️ 綜合心得生成失敗：{e}")
        return ""
