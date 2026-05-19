from datetime import datetime, timedelta
from .storage import load_record_for_date


def generate_weekly_report():
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    total_sessions = 0
    highlights = []
    weaknesses = []

    for d in dates:
        r = load_record_for_date(d)
        if not r:
            continue
        total_sessions += 1

        for ex in r.get("exercises", []):
            name = ex.get("name")
            diff = ex.get("left_right_diff")

            if diff in ["左弱", "右弱"]:
                weaknesses.append(f"{d} - {name} 出现 {diff}")
            else:
                highlights.append(f"{d} - {name} 发力正常")

    report = f"本周训练次数：{total_sessions}\n" \
             f"发力正常记录：{len(highlights)} 项\n" \
             f"左右差异记录：{len(weaknesses)} 项\n\n"

    if weaknesses:
        report += "[需要注意的动作]\n" + "\n".join(weaknesses) + "\n"

    return report
