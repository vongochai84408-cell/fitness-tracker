import json
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA_DIR = 'data'
PLOTS_DIR = 'plots'
os.makedirs(PLOTS_DIR, exist_ok=True)


def load_all_records():
    records = []
    if not os.path.exists(DATA_DIR):
        return records
    for name in sorted(os.listdir(DATA_DIR)):
        if name.endswith('.json'):
            with open(os.path.join(DATA_DIR, name), 'r', encoding='utf-8') as f:
                records.append(json.load(f))
    return records


def plot_sessions_per_week():
    records = load_all_records()
    if not records:
        return None
    # group by week number
    weekly = {}
    for r in records:
        dt = datetime.strptime(r['date'], '%Y-%m-%d')
        year, week, _ = dt.isocalendar()
        key = f"{year}-W{week}"
        weekly[key] = weekly.get(key, 0) + 1
    xs = list(weekly.keys())
    ys = [weekly[k] for k in xs]
    plt.figure(figsize=(6,3))
    plt.plot(xs, ys, marker='o')
    plt.title('Sessions per Week')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, 'sessions_per_week.png')
    plt.savefig(out)
    return out


if __name__ == '__main__':
    p = plot_sessions_per_week()
    print(p or 'no-data')
