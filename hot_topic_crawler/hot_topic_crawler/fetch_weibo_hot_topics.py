import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_weibo_hot_topics(save_dir="data/weibo/json"):
    url = "https://s.weibo.com/top/summary"
    headers = {
        "Cookie": "XSRF-TOKEN=395279;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpWg-6J.77JHA6k4UXa.qc5NHD95QceKMESoz0eh.0Ws4DqcjMBc8cqgpD9Pi0-EH81CHWBC-4eCH8SCHWeEHWBntt;MLOGIN=1;SUB=_2A25FOaNJDeRhGeBP7FAX8i3Mwj-IHXVmNrqBrDV6PUJbktANLXatkW1NRSjrsCjcpfGmJbmV2Sntjetp_TBDaQIp;ALF=1751474201;_T_WM=40960380272;M_WEIBOCN_PARAMS=oid%3D5173090550286474%26lfid%3D231093_-_selffollowed%26luicode%3D20000174%26uicode%3D20000174;SCF=AvWx5CKzqSR-iAI-YO4gCZrZoxd2-wd0mxFTMQJxjVjQ6poOJqIuOJes5hwIJQ5aHWnRQDcXUfsqRsbIZ_Xb0Wc.;SSOLoginState=1748882201;WEIBOCN_FROM=1110006030",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"class": "list-table"})
    topics = []
    rows = soup.find_all("tr")[1:]  # 跳过表头
    for row in rows:
        title_td = row.find("td", class_="td-02")
        hot_td = row.find("td", class_="td-03")

        if title_td:
            topic = title_td.get_text(strip=True)
            link = "https://s.weibo.com" + title_td.a["href"] if title_td.a else ""
            hot_value = hot_td.get_text(strip=True) if hot_td else ""
            topics.append({
                "topic": topic,
                "link": link,
                "hot_value": hot_value
            })
    # 生成带时间戳的文件名
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"hot_topic_{ts}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(f"已保存热搜主题到 {file_path}")

if __name__ == "__main__":
    fetch_weibo_hot_topics() 