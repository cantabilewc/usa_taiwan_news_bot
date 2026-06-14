"""
Telegram Bot 發送模組
"""
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> bool:
    """
    發送 Markdown 格式訊息到 Telegram
    回傳是否成功
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 請先在 .env 設定 TELEGRAM_TOKEN 和 TELEGRAM_CHAT_ID")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        print("✅ Telegram 訊息發送成功！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Telegram 發送失敗：{e}")
        if hasattr(e, 'response') and e.response:
            print(f"   回應內容：{e.response.text}")
        return False
