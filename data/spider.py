#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/3 10:57
# @Author  : Rocky
import time
import csv
import random

import requests


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "priority": "u=1, i",
    "referer": "https://www.douyin.com/jingxuan/search/COSER?aid=1d5e21f5-10bf-4838-a9ed-1a4b321b5e62&type=general&ug_source=microsoft_mz03",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "uifid": "e3b4cbff814331e10738d4b0ca1195207b8054e7f97d772f5caebc86037fab868c16f1a9324847a7a0162bc606f40ca28ffe7280c865b3555e97f2f981034f1fd9f24fba286f2f4b9a456b10bd675c7d835a93593a9c3d3b27629a3ef2b49d068935a249e026a22ca45b2d84e672cc198d039de603ed76d6a61c55b15c3a0a8d6f3343d0211b1ea09c7e637ddd4b6e78f6430db02208fa8677bd4ee1a27e723c994506f2f1bbe7c35f29d799cf2a8772eb9f6121f34493afae219bfef23a168b",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36 Edg/143.0.0.0"
}
cookies = {
    "enter_pc_once": "1",
    "UIFID_TEMP": "e3b4cbff814331e10738d4b0ca1195207b8054e7f97d772f5caebc86037fab868c16f1a9324847a7a0162bc606f40ca28ffe7280c865b3555e97f2f981034f1ffd512d0639fc1f3ce65ce8c99c22c2e42dedc509dc58d28b37cd9ce5b2c90242c46ab895cc637f93ba18ed223c33280d",
    "s_v_web_id": "verify_mjh45f7a_TAQK1CHM_6ExF_4Kqf_BW3S_6SKXhZnBVcsr",
    "hevc_supported": "true",
    "fpk1": "U2FsdGVkX1+cpOWPPrsgnQRUPSpSMc1MRZilJuSjZDGWjxO+DED5Kk+ixTCNlwVyel4QN+1IfSf241D9ODoLfQ==",
    "fpk2": "76a02e3b7c9b39b51bd1ef658e740b35",
    "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.725%7D",
    "bd_ticket_guard_client_web_domain": "2",
    "passport_csrf_token": "",# 浏览器f12查看自己的token
    "passport_csrf_token_default": "", # 浏览器f12查看自己的token
    "UIFID": "e3b4cbff814331e10738d4b0ca1195207b8054e7f97d772f5caebc86037fab868c16f1a9324847a7a0162bc606f40ca28ffe7280c865b3555e97f2f981034f1fd9f24fba286f2f4b9a456b10bd675c7d835a93593a9c3d3b27629a3ef2b49d068935a249e026a22ca45b2d84e672cc198d039de603ed76d6a61c55b15c3a0a8d6f3343d0211b1ea09c7e637ddd4b6e78f6430db02208fa8677bd4ee1a27e723c994506f2f1bbe7c35f29d799cf2a8772eb9f6121f34493afae219bfef23a168b",
    "__ac_nonce": "0695885ad0028ac953081",
    "__ac_signature": "_02B4Z6wo00f0175OcDgAAIDBaFHnepTQhre-bnSAAIbTL5w2P0NiWDE2EicYP2uaRJ6R9ellUI1sCT-Mk1qzs-CCB1z9LMFxm3L2NdGyuxwwvHOJvngFkGX2dyQ5N41aavge8BBr7TanWUl.34",
    "douyin.com": "",
    "xg_device_score": "7.617813619582719",
    "device_web_cpu_core": "12",
    "device_web_memory_size": "8",
    "architecture": "amd64",
    "dy_swidth": "1536",
    "dy_sheight": "864",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22",
    "strategyABtestKey": "%221767409077.759%22",
    "ttwid": "1%7CYDjcKKiTo_Jo_SQsEHzYCiAl87FFBV4onjfggO-x1qU%7C1767409081%7C8e01e63628ca028aa006874634045c148769ee6f2c854748db4b89095785f07f",
    "passport_mfa_token": "Cjfvub%2FciBJOfzl050DStEQpsKjc8R9a1Conn50PowQo%2F48BBHjirpI6bm4VknLx%2B8M3Eu5JTkdLGkoKPAAAAAAAAAAAAABP6OG%2F7Y9EoXAM0ogmCDkmHQwDu3HxqCnjAW7YOWbzEjK%2FRBx7uPKDmTT5KLfPy%2BaRKxCD8oUOGPax0WwgAiIBA58SYrI%3D",
    "d_ticket": "fd1f9c07f386d51e410a115f446227be53642",
    "passport_assist_user": "", # 浏览器中自己查看
    "n_mh": "L-9iYh5Y5gIT3HaffoMedu3zZ9pwUWINpZnLUlvm0lY",
    "sid_guard": "fdd22d200dcf2c3b7e6364648cd327a8%7C1767409215%7C5184000%7CWed%2C+04-Mar-2026+03%3A00%3A15+GMT",
    "uid_tt": "adfe18918d64db41fcc292135a7ec0de",
    "uid_tt_ss": "adfe18918d64db41fcc292135a7ec0de",
    "sid_tt": "fdd22d200dcf2c3b7e6364648cd327a8",
    "sessionid": "fdd22d200dcf2c3b7e6364648cd327a8",
    "sessionid_ss": "fdd22d200dcf2c3b7e6364648cd327a8",
    "session_tlb_tag": "sttt%7C3%7C_dItIA3PLDt-Y2RkjNMnqP________-sDl8bo-R_K0IN7KaH5FiD2bE0mIQEq2nps6w5OCqgisw%3D",
    "is_staff_user": "false",
    "sid_ucp_v1": "1.0.0-KGNkYTY1NTI3NTI4ZTA5NGNlYjY2NDk3YzMxNmNjMGUwMGIwY2I5YjYKIQjosoCGg_TKBhC_jOLKBhjvMSAMMISajOgFOAdA9AdIBBoCbHEiIGZkZDIyZDIwMGRjZjJjM2I3ZTYzNjQ2NDhjZDMyN2E4",
    "ssid_ucp_v1": "1.0.0-KGNkYTY1NTI3NTI4ZTA5NGNlYjY2NDk3YzMxNmNjMGUwMGIwY2I5YjYKIQjosoCGg_TKBhC_jOLKBhjvMSAMMISajOgFOAdA9AdIBBoCbHEiIGZkZDIyZDIwMGRjZjJjM2I3ZTYzNjQ2NDhjZDMyN2E4",
    "_bd_ticket_crypt_cookie": "3ce3e0196e10602f745e0ae7a0218379",
    "__security_mc_1_s_sdk_sign_data_key_web_protect": "705abd44-4ad7-8e27",
    "__security_mc_1_s_sdk_cert_key": "7808650c-470d-a323",
    "__security_mc_1_s_sdk_crypt_sdk": "be345904-4ac0-9e8d",
    "__security_server_data_status": "1",
    "login_time": "1767409214756",
    "publish_badge_show_info": "%220%2C0%2C0%2C1767409215461%22",
    "DiscoverFeedExposedAd": "%7B%7D",
    "SelfTabRedDotControl": "%5B%5D",
    "IsDouyinActive": "true",
    "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAADAXBmN3vs5WbvIef9OqluoH-8yYXWhc6szIwAozAlmAWGZXHdoBwAIlmqv4Edqtt%2F1767456000000%2F0%2F1767409220520%2F0%22",
    "home_can_add_dy_2_desktop": "%221%22",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQW9FQXRJYjFhSENLZmtkYnpuQUh6ZWY0MW1rT1ZRcGZ0STFQMktpNS9pemZNTWVBSGtDdEVUNGN3WjhzVGw3djVNVXRmZ3Nnay9VektieDFvMm9oUFE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "odin_tt": "faf6e3bd7f2140175ea66f5c8e45fa77f632b159afdef08831a3d3147edd650a495d12b776016287adaf15c714520ec7d6466116fd54242211ee0dfb3533cc7d",
    "is_dash_user": "1",
    "biz_trace_id": "857c6ed1",
    "bd_ticket_guard_client_data_v2": "eyJyZWVfcHVibGljX2tleSI6IkJBb0VBdEliMWFIQ0tma2Riem5BSHplZjQxbWtPVlFwZnRJMVAyS2k1L2l6Zk1NZUFIa0N0RVQ0Y3daOHNUbDd2NU1VdGZnc2drL1V6S2J4MW8yb2hQUT0iLCJ0c19zaWduIjoidHMuMi45ZWI1ZjNlZjNjNjAyZTdjZjA1MGI0OWY5YjVhZDQzZjEyNzIzNTBjNTJlN2FmNjMyY2FiYTIxY2ZlMmYzOTdjYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJSdk5IQ0NmUFhQSGd6K1lKYnNJVjNCOFdYd0k4YUpqQi9wSldMUEV3VWtzPSIsInNlY190cyI6IiNQVkZFcm50bDNkSkpMOGVtbEpPb3MveVlEZHJpaW5mSlBHamVwUUwzRUZMVnhZNUdRNGMrQWF6b0NBa0wifQ%3D%3D",
    "download_guide": "%222%2F20260103%2F0%22",
    "SEARCH_RESULT_LIST_TYPE": "%22single%22"
}
url = "https://www.douyin.com/aweme/v1/web/search/item/"

def get_time(ctime):
    time_lacal = time.localtime(ctime)

    time_format = time.strftime("%Y-%m-%d ", time_lacal)
    return str(time_format)
def get_json(keyword, offset, count):
    # offset和关键字联动
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_general",
        "enable_history": "1",
        "keyword": keyword,
        "search_source": "normal_search",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "disable_rs": "0",
        "offset": offset,
        "count": count,
        "need_filter_settings": "0",
        "list_type": "single",
        "pc_search_top_1_params": "{\"enable_ai_search_top_1\":1}",
        "search_id": "20260103110053387B5DD2A7F0725A5D51",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "12",
        "version_code": "190600",
        "version_name": "19.6.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "143.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "143.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "100",
        "webid": "7586653262305838618",
        "uifid": "",
        "msToken": "", # 批量采集的加密值
        "a_bogus": ""  # 批量采集的加密值
    }
    time.sleep(random.randint(1, 7))
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    print(response.text)
    print(response)
    return response.json()

# 解析数据
def paramsData(response):
    global video_dit
    minutes = response['video']['duration'] // 1000 //60
    seconds = response['video']['duration'] // 1000 % 60
    video_dit = {
        '用户名': response['author']['nickname'],
        '粉丝数量': response['author']['follower_count'],
        '视频描述': response['desc'],
        '发布时间': get_time(response['create_time']),
        '视频时长': "{:02d}:{:02d}".format(minutes, seconds),
        '点赞数': response['statistics']['digg_count'],
        '收藏数': response['statistics']['collect_count'],
        '评论数': response['statistics']['comment_count'],
        '分享数': response['statistics']['share_count'],
        '视频ID': response['aweme_id']
    }
    print(video_dit)
    # 写入数据
    writer.writerow(video_dit)

# 搜索内容
def search(keyword):
    offset = 0
    count = 10
    while True:
        response = get_json(keyword , offset, count)
        feeds = response['data']
        for feed in feeds:
            paramsData(feed['aweme_info'])
        # 判断是否还有更多数据
        if response['has_more'] == 0:
            break

        offset += count
        count = 10


if __name__ == '__main__':

    # 表头
    header = ['用户名', '粉丝数量', '视频描述', '发布时间', '视频时长', '点赞数', '收藏数', '评论数', '分享数', '视频ID']
    f = open('video_data.csv', 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(f, header)
    writer.writeheader()

    keyword = input('请输入搜索内容：')
    search(keyword)
    # print(get_time(1760783870))