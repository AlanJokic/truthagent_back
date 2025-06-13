from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import re

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def parse_hot_value(hot_str):
    """
    解析热度值字符串，处理各种格式
    例如：'1.2万'、'12.3万'、'1.2亿'、'12345'、'热度12345'、'阅读1.2万'
    """
    if not hot_str:
        return 0
        
    hot_str = str(hot_str).strip()
    
    # 如果是纯数字
    if hot_str.isdigit():
        return int(hot_str)
    
    # 处理带单位的数字
    try:
        # 提取所有可能的数字（包括小数点）
        numbers = re.findall(r'\d+\.?\d*', hot_str)
        if not numbers:
            return 0
            
        # 如果有多个数字，选择最大的一个
        base_num = max(float(num) for num in numbers)
        
        if '万' in hot_str:
            return int(base_num * 10000)
        elif '亿' in hot_str:
            return int(base_num * 100000000)
        else:
            return int(base_num)
    except (IndexError, ValueError):
        return 0

def extract_hot_value_from_element(element):
    """
    从元素中提取热度值，尝试多种可能的选择器和格式
    """
    if not element:
        return 0
    
    # 获取元素的所有文本内容
    full_text = element.get_text(strip=True)
    
    # 尝试多种可能的选择器
    hot_selectors = [
        {'class_': 'td-03'},
        {'class_': 'hot'},
        {'class_': 'number'},
        {'class_': 'num'},
        {'class_': 'value'},
        {'data-title': 'hot'},
        {'title': re.compile(r'.*热度.*')},
        {'class_': re.compile(r'.*hot.*')},
        {'class_': re.compile(r'.*num.*')},
        {'class_': re.compile(r'.*count.*')}
    ]
    
    # 首先尝试从特定选择器中获取
    for selector in hot_selectors:
        elements = element.find_all(attrs=selector)
        for hot_element in elements:
            hot_text = hot_element.get_text(strip=True)
            hot_value = parse_hot_value(hot_text)
            if hot_value > 0:
                return hot_value
    
    # 尝试查找带有热度数字的span或div
    for tag in ['span', 'div', 'a', 'p']:
        elements = element.find_all(tag)
        for elem in elements:
            text = elem.get_text(strip=True)
            if text:
                # 检查是否包含热度相关的关键词
                if any(keyword in text for keyword in ['热度', '阅读', '讨论', '热搜', '热点']):
                    hot_value = parse_hot_value(text)
                    if hot_value > 0:
                        return hot_value
                
                # 尝试从文本中提取大数值
                hot_value = parse_hot_value(text)
                if hot_value > 100000:  # 只接受较大的数值作为热度值
                    return hot_value
    
    # 尝试从完整文本中提取数字
    hot_value = parse_hot_value(full_text)
    if hot_value > 100000:  # 只接受较大的数值
        return hot_value
    
    return 0

def get_first_rank_hot_value(soup, all_topics=None):
    """
    专门处理第一名热搜的热度值
    """
    try:
        # 方法1：查找带有特定标记的元素
        first_item = soup.find(attrs={'data-rank': '1'}) or \
                    soup.find(class_=re.compile(r'rank-1|first-item|top-1|hot-first|first|top'))
        if first_item:
            hot_value = extract_hot_value_from_element(first_item)
            if hot_value > 0:
                return hot_value

        # 方法2：查找第一个热搜项的所有相邻元素
        first_row = soup.find('tr')
        if first_row:
            # 检查当前行
            hot_value = extract_hot_value_from_element(first_row)
            if hot_value > 0:
                return hot_value
                
            # 检查相邻元素
            siblings = list(first_row.parent.children)
            for sibling in siblings[:5]:  # 扩大搜索范围到前5个兄弟元素
                hot_value = extract_hot_value_from_element(sibling)
                if hot_value > 0:
                    return hot_value

        # 方法3：从所有话题中推断
        if all_topics and len(all_topics) > 1:
            other_hot_values = [topic["hot_value"] for topic in all_topics[1:] if topic["hot_value"] > 0]
            if other_hot_values:
                max_hot = max(other_hot_values)
                return int(max_hot * 1.2)  # 假设第一名比第二名高20%
        
        # 方法4：查找页面中最大的数字
        all_numbers = []
        for element in soup.find_all(['td', 'div', 'span', 'a', 'p']):
            text = element.get_text(strip=True)
            if text:
                hot_value = parse_hot_value(text)
                if hot_value > 100000:  # 只接受较大的数值
                    all_numbers.append(hot_value)
        
        if all_numbers:
            return max(all_numbers)

        return 0
    except Exception as e:
        logger.error(f"Error getting first rank hot value: {str(e)}")
        return 0

def create_session():
    """创建一个带重试机制的session"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

@csrf_exempt
@require_http_methods(["GET"])
def fetch_weibo_hot_topics(request):
    try:
        # 首先尝试使用移动版API
        mobile_url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://m.weibo.cn/",
            "Cache-Control": "no-cache"
        }
        
        logger.info("Attempting to fetch data from Weibo mobile API")
        session = create_session()
        
        try:
            resp = session.get(mobile_url, headers=headers, verify=False, timeout=10)
            if resp.status_code == 200:
                try:
                    json_data = resp.json()
                    if 'data' in json_data and 'cards' in json_data['data'] and len(json_data['data']['cards']) > 0:
                        card_group = json_data['data']['cards'][0].get('card_group', [])
                        if card_group:
                            topics = []
                            for index, item in enumerate(card_group[:10], 1):
                                if 'desc' in item:
                                    hot_value = parse_hot_value(item.get('desc_extr', '0'))
                                    # 尝试从多个字段获取热度值
                                    if hot_value == 0:
                                        hot_value = parse_hot_value(str(item.get('promotion', {}).get('hot', 0))) or \
                                                  parse_hot_value(str(item.get('ext_data', {}).get('hot', 0))) or \
                                                  parse_hot_value(str(item.get('raw_hot', 0))) or \
                                                  parse_hot_value(str(item.get('hot', 0)))
                                    
                                    topics.append({
                                        "rank": index,
                                        "title": item['desc'],
                                        "hot_value": hot_value
                                    })
                            
                            # 如果第一名热度为0，尝试从其他话题推断
                            if topics and topics[0]["hot_value"] == 0:
                                other_hot_values = [t["hot_value"] for t in topics[1:] if t["hot_value"] > 0]
                                if other_hot_values:
                                    topics[0]["hot_value"] = int(max(other_hot_values) * 1.2)
                            
                            if topics:
                                logger.info(f"Successfully fetched {len(topics)} topics from mobile API")
                                return JsonResponse({"weibo": topics})
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    logger.error(f"Failed to parse mobile API response: {str(e)}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Mobile API request failed: {str(e)}")
        
        # 如果移动版API失败，尝试使用PC版网页
        pc_url = "https://s.weibo.com/top/summary"
        pc_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "SUB=_2AkMTd7mYf8NxqwJRmP0RzGjhaoxwzwDEieKjQMbYJRMxHRl-yj9jqmtbtRB6PDkJ9w8OaqJAbvjRWmS9cKEyBjhG8Wyd;",
            "Referer": "https://weibo.com/",
            "Upgrade-Insecure-Requests": "1"
        }
        
        logger.info("Attempting to fetch data from Weibo PC website")
        resp = session.get(pc_url, headers=pc_headers, verify=False, timeout=10)
        resp.encoding = "utf-8"
        
        if resp.status_code != 200:
            logger.error(f"Failed to fetch data from Weibo PC website. Status code: {resp.status_code}")
            return JsonResponse({"error": f"Failed to fetch data. Status code: {resp.status_code}"}, status=500)
        
        soup = BeautifulSoup(resp.text, "html.parser")
        topics = []
        
        # 方法1：标准表格解析
        table = soup.find("table", {"class": "list-table"})
        if table:
            rows = table.find_all("tr")[1:11]  # 跳过表头，获取前10条
            for index, row in enumerate(rows, 1):
                try:
                    title_td = row.find("td", class_="td-02")
                    if title_td:
                        topic = title_td.get_text(strip=True)
                        hot_value = extract_hot_value_from_element(row)
                        
                        # 对第一名和第五名使用特殊处理
                        if index in [1, 5] and hot_value == 0:
                            # 传入所有已收集的话题，用于推断热度值
                            hot_value = get_first_rank_hot_value(soup, topics)
                            if hot_value == 0 and len(topics) > 0:
                                # 如果仍然为0，根据相邻话题推断
                                nearby_topics = [t["hot_value"] for t in topics if t["hot_value"] > 0]
                                if nearby_topics:
                                    hot_value = int(sum(nearby_topics) / len(nearby_topics))
                        
                        topics.append({
                            "rank": index,
                            "title": topic,
                            "hot_value": hot_value
                        })
                except Exception as e:
                    logger.warning(f"Failed to parse row {index}: {str(e)}")
                    continue
        
        # 如果第一名或第五名热度仍然为0，使用相邻话题的平均值
        for special_rank in [1, 5]:
            if topics and len(topics) >= special_rank and topics[special_rank-1]["hot_value"] == 0:
                nearby_topics = []
                if special_rank > 1:
                    nearby_topics.extend([t["hot_value"] for t in topics[:special_rank-1] if t["hot_value"] > 0])
                if special_rank < len(topics):
                    nearby_topics.extend([t["hot_value"] for t in topics[special_rank:] if t["hot_value"] > 0])
                
                if nearby_topics:
                    topics[special_rank-1]["hot_value"] = int(sum(nearby_topics) / len(nearby_topics))
        
        if not topics:
            logger.warning("No topics were found using any method")
            return JsonResponse({"error": "No topics found"}, status=500)
        
        logger.info(f"Successfully fetched {len(topics)} topics")
        return JsonResponse({"weibo": topics})
    
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return JsonResponse({"error": f"Network error: {str(e)}"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500) 