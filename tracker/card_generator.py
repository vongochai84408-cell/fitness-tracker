from datetime import datetime
from .config import MUSCLE_SCHEDULE


# 简化版训练卡片（与你 Telegram cron 逻辑一致）
def generate_daily_card():
    weekday = datetime.now().isoweekday()  # 1-7
    if weekday == 7:
        muscle = "休息/总结"
    else:
        muscle = MUSCLE_SCHEDULE.get(weekday, "未知肌群")

    actions = {
        "胸": ["卧推", "上斜卧推", "飞鸟"],
        "背": ["引体", "划船", "下拉"],
        "腿": ["深蹲", "腿举", "硬拉轻量"],
        "肩": ["推举", "侧平举", "反向飞鸟"],
        "手臂": ["弯举", "臂屈伸", "hammer curl"],
        "核心/心肺": ["卷腹", "平板支撑", "空腹跑步"]
    }

    act = actions.get(muscle, [])

    text = f"今日肌群：{muscle}\n建议动作：" + "、".join(act)
    return text
