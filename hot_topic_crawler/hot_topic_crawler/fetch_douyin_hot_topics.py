import requests
import os
import json
from datetime import datetime

def fetch_douyin_hot_topics(save_dir="data/douyin/json"):
    url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=en-US&browser_platform=MacIntel&browser_name=Chrome&browser_version=114.0.0.0&browser_online=true&engine_name=Blink&engine_version=114.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=4&device_memory=8&platform=PC&downlink=1.5&effective_type=3g&round_trip_time=600&webid=7246602757481154103&msToken=A-dVF1R3L6t6yeYNVsnPA7YMBkohetjMSING0Q3C3UGXBq7B_lhuJVv6N1hF8Yum9qxQMMVa_GiSsER1Yf595bF5Q_O3-JY1hQ8s-ZPB21PCVYL5C7PEjQiPAMGtGg==&X-Bogus=DFSzswVOXn0ANcrmtjl2YN7TlqSE'
    headers = {
        'Cookie': 'UIFID=23655950011bb904512d521d3cef160ff5e8f8f1019b61f52f50cf5b516fc590554ad7634b8a95b9296a4abccb8069faaf68253204a7b2af774c885234d6d51f45ec163ba6094784ea0fa1098ba8a1364bda66a35ec815ccd860b2183c2b4ad65a2ae91036b7352f5ee9c83559c6e3e40be47398d8bc18622d63137b5c9bbb48898ab6179a324886a26c916d7ccc1ffa01d13537742c271dca5a641ede9fe29a;__security_server_data_status=1;SEARCH_RESULT_LIST_TYPE=%22single%22;SelfTabRedDotControl=%5B%5D;is_staff_user=false;sessionid_ss=b49198e02b533691ef63bb4216e12f6e;login_time=1749145659673;=douyin.com;passport_auth_status_ss=8585893af97c0bb53117be6df93acf63%2C;s_v_web_id=verify_mbjf6nar_BRIDptG0_UfDu_4uHj_BdSS_xNoAeUVOTE92;passport_csrf_token=3f966980d20d11b0b89c503fc546a680;home_can_add_dy_2_desktop=%221%22;xgplayer_user_id=891542719542;fpk1=U2FsdGVkX1+1nPszLHwWmzyQYMk98QDjPP/P5EFRL0zpN+wq3VR0Q08oDGw08El6Yvwx6rraOnSnDPvhUgAu/Q==;_bd_ticket_crypt_cookie=7604ba82311bff548896db6b271e8627;passport_fe_beating_status=true;sid_ucp_v1=1.0.0-KDJjMzA1YTMzZjRiY2MzMzhiMmYzMjMzYTkzNjczMWVjYjk4NzdhZTEKIQidmqDi642iAxC7sIfCBhjvMSAMMKOIr48GOAJA8QdIBBoCbHEiIGI0OTE5OGUwMmI1MzM2OTFlZjYzYmI0MjE2ZTEyZjZl;device_web_memory_size=8;FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAj1aWdmlK2Ksj15PeY1PTO21BbgEJBjV6pmpViTa3ndCwkPkREXlf4Ti523XbMaYe%2F1749225600000%2F0%2F1749215907791%2F0%22;hevc_supported=true;passport_mfa_token=Cje1ofkS6GMF1%2B2JwUGr1xEM6Lr4Zs%2B4CYrXlQ8ntPFgHs3uhpctZRYLbIk4BDCjSUo3xsLOH3OYGkoKPAAAAAAAAAAAAABPFE14vSCtubeNdRmoAF9MeA%2BrPssaO9BLWt7swoRN1uMeaO3uo%2FVr3wAxVbvop2XeWRDrpvMNGPax0WwgAiIBA%2F%2FQRp4%3D;xg_device_score=7.4867892174847075;WallpaperGuide=%7B%22showTime%22%3A1749145436777%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A22%2C%22cursor2%22%3A6%2C%22hoverTime%22%3A1749216813583%7D;volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D;bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCUFRPb29pa2RWMGx0K2JUUjJNcjRLZUhxUEpJTzk2SDhMeUR5aTRsbk0yV0VMUHpybGtSUWIrcEN5YU1NaldWS3NTUkVHbHltSkdTcSs3SzJWV1FHTnM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D;sid_guard=b49198e02b533691ef63bb4216e12f6e%7C1749145659%7C5184000%7CMon%2C+04-Aug-2025+17%3A47%3A39+GMT;ttwid=1%7CqVczPuGb59tmz6U0KIEQ2P0igPOQGkNN7Qly5DtF7bE%7C1737825834%7Cd6c346e8757cd16d16d36b13cdf5d4a8aee85ecd659490fda0202d0035134307;store-region-src=uid;is_dash_user=1;stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1710%2C%5C%22screen_height%5C%22%3A1107%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.45%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A700%7D%22;__ac_nonce=06842ea9f0012c48bdd24;__ac_signature=_02B4Z6wo00f01XPQDugAAIDAWtSQlsZmPV1z8ApAADS62d;__druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0EyOTglMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E1MzIlMkMlMjJ3aWR0aCUyMiUzQTI5OCUyQyUyMmhlaWdodCUyMiUzQTUzMiUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0EyJTJDJTIydXNlckFnZW50JTIyJTNBJTIyTW96aWxsYSUyRjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzcpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGMTM0LjAuMC4wJTIwU2FmYXJpJTJGNTM3LjM2JTIwRWRnJTJGMTM0LjAuMC4wJTIyJTdE;__security_mc_1_s_sdk_cert_key=ccf2b816-422a-9971;__security_mc_1_s_sdk_crypt_sdk=4b9f8331-4c92-9a15;__security_mc_1_s_sdk_sign_data_key_web_protect=3679d82c-4996-9246;_bd_ticket_crypt_doamin=2;bd_ticket_guard_client_web_domain=2;biz_trace_id=4ce4657a;d_ticket=2c6eccff55db44858a619d4d0503226e9026b;device_web_cpu_core=8;download_guide=%222%2F20250606%2F1%22;dy_sheight=1107;dy_swidth=1710;FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D;fpk2=ca9d7b697f560eddb43ea19d8dcf8ff2;IsDouyinActive=true;n_mh=SjcuQC6HvA7_cmjmOwytAtPa6dSOv68uSw4B56cRVhI;odin_tt=9d89bea3b4bffe118084fe7aa873e6f04674f8bd466cd13281107de873e7e3248056d6892c20c1bc3053fcf9765b28a85a3c45ffa989aed8722539dc8e98ef19;passport_assist_user=CkGBv42vTmdujQFimqIzWhxOHtYeTn-D39q5xkhskw0AA0TYxa8-dB4Jd1hKbtbHTV2Jcs6zm6M3DNuUtvms2uaiFxpKCjwAAAAAAAAAAAAATxSgr5DT1cFIR5zbAKtAQLoY2bN4laznFQDoz16Sjd-6emfI_oAX6s1tQS6pucFOxPIQ66bzDRiJr9ZUIAEiAQPj0to_;passport_auth_status=8585893af97c0bb53117be6df93acf63%2C;passport_csrf_token_default=3f966980d20d11b0b89c503fc546a680;publish_badge_show_info=%220%2C0%2C0%2C1749145672372%22;sessionid=b49198e02b533691ef63bb4216e12f6e;sid_tt=b49198e02b533691ef63bb4216e12f6e;ssid_ucp_v1=1.0.0-KDJjMzA1YTMzZjRiY2MzMzhiMmYzMjMzYTkzNjczMWVjYjk4NzdhZTEKIQidmqDi642iAxC7sIfCBhjvMSAMMKOIr48GOAJA8QdIBBoCbHEiIGI0OTE5OGUwMmI1MzM2OTFlZjYzYmI0MjE2ZTEyZjZl;store-region=cn-sc;strategyABtestKey=%221749145407.825%22;uid_tt=33d1ddcedd6139de3f39de2b52c40a20;uid_tt_ss=33d1ddcedd6139de3f39de2b52c40a20;UIFID_TEMP=23655950011bb904512d521d3cef160ff5e8f8f1019b61f52f50cf5b516fc59056a7aa162cab350cdaa1252890b8a522f366b0b9b17afc20ce88a4ca5745ac35b4460006f8c75ae8d8183d84a2f5d47a',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()

    trending_list = data.get("data", {}).get("trending_list", [])
    word_list = data.get("data", {}).get("word_list", [])

    topics = []

    # # 处理 trending_list
    # for item in trending_list:
    #     topics.append({
    #         "type": "trending",
    #         "word": item.get("word"),
    #         "hot_value": item.get("hot_value"),
    #         "group_id": item.get("group_id"),
    #         "cover": item.get("word_cover", {}).get("url_list", [None])[0],
    #         "event_time": item.get("event_time"),
    #     })

    # 处理 word_list
    for item in word_list:
        topics.append({
            "type": "hot",
            "word": item.get("word"),
            "hot_value": item.get("hot_value"),
            "group_id": item.get("group_id"),
            "cover": item.get("word_cover", {}).get("url_list", [None])[0] if item.get("word_cover") else None,
            "view_count": item.get("view_count"),
            "position": item.get("position"),
        })

    # 保存为 JSON 文件
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"hot_topic_{ts}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存抖音热榜到：{file_path}")

if __name__ == "__main__":
    fetch_douyin_hot_topics()