# Telegram Bot for fitness-tracker
import os
import json
import requests
from datetime import datetime
from tracker.parser import parse_reply
from tracker.storage import save_training_record
from tracker.card_generator import generate_daily_card
from tracker.weekly_report import generate_weekly_report

BOT_TOKEN = os.getenv("FITNESS_BOT_TOKEN")
CHAT_ID = os.getenv("FITNESS_CHAT_ID")

API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else None


def send_message(text):
    if not API or not CHAT_ID:
        print("未设置 Bot 环境变量")
        return
    requests.post(f"{API}/sendMessage", json={"chat_id": CHAT_ID, "text": text})


def handle_message(text):
    if text == "卡片":
        send_message(generate_daily_card())
        return
    if text == "周报":
        send_message(generate_weekly_report())
        return

    ex = parse_reply(text)
    if ex:
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "muscle_group": "",
            "exercises": [ex]
        }
        save_training_record(record)
        send_message(f"已记录：{ex['name']} {ex['sets']}")

