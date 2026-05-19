from datetime import datetime
from tracker.parser import parse_reply
from tracker.storage import save_training_record
from tracker.card_generator import generate_daily_card
from tracker.weekly_report import generate_weekly_report

# 入口脚本，用于与你的 Telegram Bot 对接
# 示例使用：
# python main.py --record "卧推 40x6x3 左弱"
# python main.py --card
# python main.py --week

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", type=str, help="记录训练，例如：卧推 40x6x3 左弱")
    parser.add_argument("--card", action="store_true", help="生成今日训练卡片")
    parser.add_argument("--week", action="store_true", help="生成周报")
    args = parser.parse_args()

    if args.record:
        ex = parse_reply(args.record)
        if not ex:
            print("无法解析输入格式")
            return
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "muscle_group": "",
            "exercises": [ex]
        }
        save_training_record(record)
        print("已记录：", ex)

    elif args.card:
        print(generate_daily_card())

    elif args.week:
        print(generate_weekly_report())

    else:
        print("未提供参数。--record / --card / --week")


if __name__ == "__main__":
    main()