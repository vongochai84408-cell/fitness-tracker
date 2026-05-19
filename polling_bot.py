# Long-polling runner for fitness-tracker Telegram bot
# Usage:
#   TELEGRAM_PROXY=http://192.168.1.247:18780 \
#   FITNESS_BOT_TOKEN=xxxxx \
#   FITNESS_CHAT_ID=7177755169 \
#   python polling_bot.py

import os
import time
import requests

from bot.telegram_bot import BOT_TOKEN, CHAT_ID, API, PROXIES, handle_message, send_message

GET_UPDATES = f"{API}/getUpdates" if API else None

# Only accept messages from this chat/user to avoid abuse
ALLOWED_CHAT = CHAT_ID

def poll():
    if not BOT_TOKEN or not CHAT_ID:
        print("环境变量缺失：FITNESS_BOT_TOKEN / FITNESS_CHAT_ID")
        return
    if API is None:
        print("未生成 Telegram API 基础地址")
        return

    offset = None
    print("[fitness-bot] Polling started…")
    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            r = requests.get(GET_UPDATES, params=params, proxies=PROXIES, timeout=40)
            r.raise_for_status()
            data = r.json()
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg:
                    continue
                chat_id = str(msg.get("chat", {}).get("id"))
                text = (msg.get("text") or "").strip()
                if not text:
                    continue
                # Only handle messages from the configured chat
                if ALLOWED_CHAT and str(ALLOWED_CHAT) != chat_id:
                    # Optionally notify unknown sender
                    continue
                print(f"[recv] {chat_id}: {text}")
                handle_message(text)
        except Exception as e:
            print(f"[poll-error] {e}")
            time.sleep(2)


if __name__ == "__main__":
    poll()
