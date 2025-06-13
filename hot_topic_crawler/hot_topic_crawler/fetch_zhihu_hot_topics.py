import requests
from bs4 import BeautifulSoup
import os
import re
import json
from datetime import datetime

def fetch_zhihu_hot_topics(save_dir="data/zhihu/json"):
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Referer': 'https://www.zhihu.com/hot',
        'Cookie': 'expire_in=15552000;assva5=U2FsdGVkX19T+6IRP2fVcr7V0ejdonglVXKswMhLsPcJCnrEMHR6FjVbbg6+yAQ4CbHUBwwozA1p9iUBMltI1w==;q_c1=432035f2ed624043b07106e69df86534|1738700555000|1738700555000;ref_source=other_https://www.zhihu.com/signin;tst=h;edu_user_uuid=edu-v1|82cda8c7-c893-4bb3-bb97-7fa25a98031d;z_c0=2|1:0|10:1749017518|4:z_c0|92:Mi4xdU1la1N3QUFBQUFBOE5HZVh4ZmVHU1lBQUFCZ0FsVk5yakV0YVFCZTg4SzhaSEswQWNxeUVscHplRDBCLTliOHN3|b181c78a2cb7fc5e6646b7157cc4a3cceae746b0e14fa47cf50988a22cfeddad;osd=UFwWAU647iuGINLdErjfOM1w_zoK0JFMtHSbvl_Uuh_OXZSfLO89bO4h09sUo2NO6NWO-_uTvL1v9UV8s35U2E4=;Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1749145048;HMACCOUNT=4A5B16A8A3D862BA;gdxidpyhxdE=fzt2uo%5CO0rtHTTwOp%2BbnP0rBfZoigSaNDHaDNnYsz2ypV9A%5C5aIeYRnd1tc1NGgH1fGjMyCCaX5rTf5XD4AK0JQ9Iqw%5CvPrY4D5n50uLdHSL57ycuuHZrEzgyrtC7QBLE8AgK5oAAvRoxsB73sZMZUrKxjAclA9Ou8eWquMuSGVCPMtn%3A1749018150938;_xsrf=LS98kvARkKDXMxBYFCmpa9XjImbbcInd;BEC=244e292b1eefcef20c9b81b1d9777823;captcha_ticket_v2=2|1:0|10:1749017501|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6Ik5BTlBfWCpJLjFpTUEuWGJsMFNiT2JwVmZUVFdaUUxlNkhiMVA4ZFFCSmc1d2kwZFNkYypBTnpKQ0h4aipLWk5HQzMwOFJrOGVselRiTVJUdmpDRDZBeDRreUJNbUltclZKS0FBaTB2ZklUZ25DdnkxZXlvUzg5ODEyM2FQejJaQWY2amZfX2psNWdZMkdCMFJ4QVNPV1h2RzVDdS5DLnJGREQ0WmcxUDVZbGFibTB5NXVVZUNPZGRnWjZZanNwamtPZkxoeFRMdEJIR3hSOFNqUVNrX3h4bW10SWxLbWdnWDJzRjZMT0RsTE12a0paYzJpWDM4WTFPU3lheVVBRXdEc0VFRmNuQkExOC42UlVva3VQWDVzRE4qSnBYMENiNElrOXBOdjBNR3VCNEtTcVFQRm1XY0pkSHIydlJPVnRJQXlWeElPVXBENmJKbm93aG9kQV9tNkllV2lJUjhuYjZKWjBnUzNTT3hrSzF5U2VVWDMwYlZuQXJBYXpKYUdSeTZQek05Z0VpRnVOY1AwUzRXZnVYdUdCanJ3amtmd2pSWFhXODNrSEZhVl9FQVNiQnAuNkN2NTRMTjVwaUpaZjBvczRKeGRHT3lPVURUb0t2b2U5OC4xTm4yRWRHUDRyUEl4b0duM2poR0pIay5BRVdtTlA2YmlOcVJidFZzZVZ4bXNuWGZFeEpxc003N192X2lfMSJ9|091bee59b800f13edc107d41da6b4f9b876a19a78c621c63d9b8d10152d649f5;captcha_session_v2=2|1:0|10:1749017481|18:captcha_session_v2|88:OExSZUdNRGV3bWJTRDN2NjZVVzBDN1pTME5QeXlCN3E2dnlXN3VDcktvUXR4UERoeFFrbEp4cnY3VG5PK21ISw==|70510812569014bbbd5517a697da3b7fdec0157e84e45d057a6d3ea46e67a1a1;JOID=U1kUCk676ymNINHYELPfO8hy9DoJ1ZNHtHeevFTUuRrMVpScKe02bO0k0dAUoGZM49WN_vmYvL5q9058sHtW004=;cmci9xde=U2FsdGVkX19CLBB9VmRwN+n+LUp7rvbz6DXERsallzaZTFG9kmgvXQUM92dU3Fi5NdyJ7Vnz1L1F+h1DQWb3zg==;__snaker__id=cm1UI2PPyVArKkrH;__zse_ck=004_PSsN1R/wM=4k8GMA1=BZxFIj/3/p3vKWy1uW/pe0N1NNEXI/smx9sH6TlSuOvzt1E2kLYKw/7WYbArXXtPiK7FwGHvNwqk92KHEGrdNkRC6y/yGfgURy12CcGaDoHwy8-CSMZ+6KEQT7wCX7QS6cLKH9JlrWuKX9yXivd3ozfKIhc3EZHfK3xh4M9QgPfKj7fVY218oZqej81Bx2f9gSsZ4R2IU3FJzdu4Pc3k/eInCSeg1lvblF+clAMjwvGzplW;_zap=58f723b0-42c3-48a2-bd6f-c89a02519f4b;assva6=U2FsdGVkX1/J0MZex7ciRmP9imh8KxftBnU+F1C42Bs=;crystal=U2FsdGVkX19Q/jUPTAEdB942p69SDXP3QzWDNILDfL/UGBU9D3dieUPb7Lg2iSCMHkDmR9yd/r7YlYXDN4uIRpQ7vfxOooV0W7cOJ2c61KgaOgnZukRnligX4lnpjslRHuh/ki0h81DvzGeWRfqK8K081AWtuwpoDVcz0Z098OQUkFzElsQO/vjSpNw30O0lx51hhuhlCqPbNif3CEBnFuExhwGTJHI0kzbp8uT2n7KiluTNYf2k9tu29PuLWPUx;d_c0=APDRnl8X3hmPTt-79Fe1_1F_BFk2ksa_hv4=|1737181024;DATE=1749015343656;Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1747233715,1747903149,1748190896,1748951106;o_act=login;pmck9xge=U2FsdGVkX1+P1bgQN3kfqQ3xoFTGl2fhE4d0CoCXDr8=;SESSIONID=nxf5SOdLkR3IzAD9T2noMhCvl8OIEqbrlnVaUOaXcMX;vmce9xdq=U2FsdGVkX1+4V60Y0ait0mlgJUMwFfkhJi8yeJ3rC59Y3R/5Vl/saqiIz4otOLD9QfwIY4PLCQ9CzQM2vyS8QQ+7MGjog5/5g5gm4mYbNz6GvpRy1q1KwJVrPNkQFeoXyQUX8tTgYzXtyqBi0Op1OATfXfG0IkDC9SdqZeCrioA=' 
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return

    try:
        data = response.json()
    except Exception as e:
        print(f"JSON解析失败：{e}")
        return

    hot_list = data.get("data", [])

    topics = []
    for item in hot_list:
        target = item.get("target", {})
        title = target.get("title", "")
        excerpt = target.get("excerpt", "")
        link = f"https://www.zhihu.com/question/{target.get('id')}" if target.get("id") else ""

        topics.append({
            "title": title,
            "excerpt": excerpt,
            "link": link
        })

    # 保存为 JSON 文件
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"hot_topic_{ts}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    print(f"✅ 已保存知乎热榜到：{file_path}")

if __name__ == "__main__":
    fetch_zhihu_hot_topics()
