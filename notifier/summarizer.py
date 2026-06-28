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


def generate_overall_insight(news_list: list[dict]) -> str:
    """
    針對整批新聞（含標題與摘要），生成一段約 1000 字的綜合心得分析
    內容包含股市影響層級評估（高/中/低）與重點產業影響
    若 API 未設定或呼叫失敗，回傳空字串（formatter 會自動跳過該區塊）
    """
    if not ANTHROPIC_API_KEY or not news_list:
        return ""

    # 把所有新聞標題+摘要整理成一份內容餵給模型
    combined = "\n\n".join(
        f"標題：{n.get('title', '')}\n摘要：{n.get('summary', '') or n.get('ai_summary', '')}"
        for n in news_list
    )

    prompt = (
        "以下是過去一週與川普政策相關的數則新聞標題與摘要。"
        "請你以財經/政策觀察者的角度，針對這些新聞寫一段約 1000 字的繁體中文綜合心得，內容須包含：\n"
        "1. 這些事件之間的關聯性\n"
        "2. 對台美股市的影響評估，並標示「影響層級」（分為：高／中／低），說明評斷理由\n"
        "3. 對重點產業或個股類型可能造成的影響（例如：半導體、AI硬體、傳產等）\n"
        "4. 值得關注的後續發展\n"
        "請直接輸出心得內容，不要加標題或前言：\n\n"
        f"{combined}"
    )

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 2500,
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
