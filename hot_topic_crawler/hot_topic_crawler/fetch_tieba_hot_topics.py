import requests
import os
import json
from datetime import datetime

def fetch_baidu_hot_topics(save_dir="data/tieba/json"):
    url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()

    cards = data.get("data", {}).get("cards", [])
    if not cards:
        print("未获取到热搜数据")
        return

    topics = []

    # 置顶热搜
    for item in cards[0].get("topContent", []):
        topics.append({
            "type": "top",
            "title": item.get("word"),
            "desc": item.get("desc"),
            "hotScore": item.get("hotScore"),
            "url": item.get("url"),
            "index": 0
        })

    # 普通热搜
    for idx, item in enumerate(cards[0].get("content", []), 1):
        topics.append({
            "type": "normal",
            "title": item.get("word"),
            "desc": item.get("desc"),
            "hotScore": item.get("hotScore"),
            "url": item.get("url"),
            "index": idx
        })

    # 保存为 JSON 文件
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"hot_topic_{ts}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存百度热搜榜到：{file_path}")

if __name__ == "__main__":
    fetch_baidu_hot_topics()
