# 解析用户在 Telegram 回复的训练记录格式
# 示例输入：
# "卧推 40x6x3 左弱"

import re


def parse_reply(text: str):
    text = text.strip()
    if not text:
        return None

    # 动作名称（非数字开头）
    match = re.match(r"([\u4e00-\u9fa5A-Za-z]+)\s*(.*)", text)
    if not match:
        return None

    name = match.group(1)
    rest = match.group(2)

    # 提取重量 × 次数 × 组数
    num_match = re.findall(r"(\d+)\s*[x×]\s*(\d+)\s*[x×]\s*(\d+)", rest)
    sets = None
    if num_match:
        w, rep, sets_n = num_match[0]
        sets = f"{w}kg × {rep} × {sets_n}"

    # 左右差异（可选）
    if "左" in rest and "弱" in rest:
        diff = "左弱"
    elif "右" in rest and "弱" in rest:
        diff = "右弱"
    else:
        diff = "正常"

    return {
        "name": name,
        "sets": sets or "未提供组数",
        "left_right_diff": diff,
        "notes": ""
    }
