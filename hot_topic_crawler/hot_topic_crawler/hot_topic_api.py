from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import uvicorn

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_weibo_hot_topics() -> Dict:
    url = "https://s.weibo.com/top/summary"
    headers = {
        "Cookie": "XSRF-TOKEN=395279;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpWg-6J.77JHA6k4UXa.qc5NHD95QceKMESoz0eh.0Ws4DqcjMBc8cqgpD9Pi0-EH81CHWBC-4eCH8SCHWeEHWBntt;MLOGIN=1;SUB=_2A25FOaNJDeRhGeBP7FAX8i3Mwj-IHXVmNrqBrDV6PUJbktANLXatkW1NRSjrsCjcpfGmJbmV2Sntjetp_TBDaQIp;ALF=1751474201;_T_WM=40960380272;",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", {"class": "list-table"})
        
        if not table:
            raise HTTPException(status_code=500, detail="Failed to fetch hot topics")
        
        topics = []
        rows = soup.find_all("tr")[1:11]  # 只获取前10条热搜
        
        for index, row in enumerate(rows, 1):
            title_td = row.find("td", class_="td-02")
            hot_td = row.find("td", class_="td-03")
            
            if title_td and hot_td:
                topic = title_td.get_text(strip=True)
                hot_value = hot_td.get_text(strip=True)
                # 将热度值转换为数字（去除"热度"等文字）
                try:
                    hot_value = int(''.join(filter(str.isdigit, hot_value)))
                except ValueError:
                    hot_value = 0
                
                topics.append({
                    "rank": index,
                    "title": topic,
                    "hot_value": hot_value
                })
        
        return {"weibo": topics}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backstage.html/api/crawl/hotlist")
async def get_hot_topics():
    return fetch_weibo_hot_topics()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080) 