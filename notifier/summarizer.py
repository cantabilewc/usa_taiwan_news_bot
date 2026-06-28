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
