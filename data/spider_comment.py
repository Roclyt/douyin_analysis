#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/3 16:11
# @Author  : Rocky
import time
import urllib
import csv
import execjs
import requests
import random
import pandas as pd


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "bd-ticket-guard-client-data": "eyJ0c19zaWduIjoidHMuMi45ZWI1ZjNlZjNjNjAyZTdjZjA1MGI0OWY5YjVhZDQzZjEyNzIzNTBjNTJlN2FmNjMyY2FiYTIxY2ZlMmYzOTdjYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50IjoidGlja2V0LHBhdGgsdGltZXN0YW1wIiwicmVxX3NpZ24iOiJJLzNmQlAzNEZDclhBa1JaSm1Xb041SVo1bGNXOG9sRnBnN0FOcWJZNVZzPSIsInRpbWVzdGFtcCI6MTc2NzQyNzUxM30=",
    "bd-ticket-guard-ree-public-key": "BAoEAtIb1aHCKfkdbznAHzef41mkOVQpftI1P2Ki5/izfMMeAHkCtET4cwZ8sTl7v5MUtfgsgk/UzKbx1o2ohPQ=",
    "bd-ticket-guard-version": "2",
    "bd-ticket-guard-web-sign-type": "1",
    "bd-ticket-guard-web-version": "2",
    "priority": "u=1, i",
    "referer": "https://www.douyin.com/jingxuan/search/coser?aid=d72bd88f-7733-4f0f-8368-1c4f16f28e9c&modal_id=7283095546892504361&type=general&ug_source=microsoft_mz03",
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
    "UIFID_TEMP": "", # 浏览器中查看
    "s_v_web_id": "verify_mjh45f7a_TAQK1CHM_6ExF_4Kqf_BW3S_6SKXhZnBVcsr",
    "hevc_supported": "true",
    "fpk1": "U2FsdGVkX1+cpOWPPrsgnQRUPSpSMc1MRZilJuSjZDGWjxO+DED5Kk+ixTCNlwVyel4QN+1IfSf241D9ODoLfQ==",
    "fpk2": "76a02e3b7c9b39b51bd1ef658e740b35",
    "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.725%7D",
    "bd_ticket_guard_client_web_domain": "2",
    "passport_csrf_token": "",# 浏览器中查看
    "passport_csrf_token_default": "",# 浏览器中查看
    "UIFID": "e3b4cbff814331e10738d4b0ca1195207b8054e7f97d772f5caebc86037fab868c16f1a9324847a7a0162bc606f40ca28ffe7280c865b3555e97f2f981034f1fd9f24fba286f2f4b9a456b10bd675c7d835a93593a9c3d3b27629a3ef2b49d068935a249e026a22ca45b2d84e672cc198d039de603ed76d6a61c55b15c3a0a8d6f3343d0211b1ea09c7e637ddd4b6e78f6430db02208fa8677bd4ee1a27e723c994506f2f1bbe7c35f29d799cf2a8772eb9f6121f34493afae219bfef23a168b",
    "douyin.com": "",
    "xg_device_score": "7.617813619582719",
    "device_web_cpu_core": "12",
    "device_web_memory_size": "8",
    "architecture": "amd64",
    "dy_swidth": "1536",
    "dy_sheight": "864",
    "strategyABtestKey": "%221767409077.759%22",
    "ttwid": "1%7CYDjcKKiTo_Jo_SQsEHzYCiAl87FFBV4onjfggO-x1qU%7C1767409081%7C8e01e63628ca028aa006874634045c148769ee6f2c854748db4b89095785f07f",
    "passport_mfa_token": "",# 浏览器中查看
    "d_ticket": "fd1f9c07f386d51e410a115f446227be53642",
    "passport_assist_user": "",# 浏览器中查看
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
    "is_dash_user": "1",
    "download_guide": "%222%2F20260103%2F0%22",
    "SEARCH_RESULT_LIST_TYPE": "%22single%22",
    "__ac_nonce": "06958cbee006b47a26ab5",
    "__ac_signature": "_02B4Z6wo00f013rHzWQAAIDBrNhaJHT02E9698nAALf09vQEpiBkQQjZD3wtBM2uJY.IVqyNgsm4AhJdtTAem1.yP2h6BkpuBdirdcTeFBJiVX2BEkoSqVqWFAXWugSlwMkq8Ka50MNWs7ypc4",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22",
    "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAADAXBmN3vs5WbvIef9OqluoH-8yYXWhc6szIwAozAlmAWGZXHdoBwAIlmqv4Edqtt%2F1767456000000%2F0%2F0%2F1767427704557%22",
    "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAADAXBmN3vs5WbvIef9OqluoH-8yYXWhc6szIwAozAlmAWGZXHdoBwAIlmqv4Edqtt%2F1767456000000%2F0%2F1767427104557%2F0%22",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQW9FQXRJYjFhSENLZmtkYnpuQUh6ZWY0MW1rT1ZRcGZ0STFQMktpNS9pemZNTWVBSGtDdEVUNGN3WjhzVGw3djVNVXRmZ3Nnay9VektieDFvMm9oUFE9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "home_can_add_dy_2_desktop": "%221%22",
    "biz_trace_id": "4ba250a3",
    "IsDouyinActive": "true",
    "odin_tt": "b7eb8704f77f752eb97a31f2386b374b4d9534cdf53ac234a077c62cc6e20393838b50785f99dc2937f14ce8c1baaac75f6d7f65935503c6092b79285beac31a",
    "sdk_source_info": "7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2736313c33373232373132333234272927676c715a75776a716a666a69273f2763646976602778",
    "bit_env": "OTdvgAv8mg0lS7mCaEKagm-mdryH9dBvgX3dcNjxUfJPlMJcAO8y_VKYdxyeQWK7qeBUTeKeQKF-kQ6PbXf0QjNk2b9YWn_CiOuTmAOqvlo_NdMMWZf-2_qV43euWIY7V5gb7hjp7PjvUS8oPQkWNs1MsCJStylSU5pE2TM0_mQvNwA43U7GSKfHnxJN4jhRf9hEE3JfjwppwqPp9bSIEt69J4kssNclv3_sj7wZSUszD7yHUli0GG2wC1By705m4GnugI2B1I5KhBo8iRFhbx7rXDe91C_p6zyND4uYMtbALFq4apzgeJmj49b2u5yuNO84Gg_7xfIbFL_pc-d5OrM8Jm7OpB4B8byb6kr5OOTLeL8nw3-FaWN6N1SCmoVUV0D_lF-AB3HkcPhJfpt5rTXuFQlPdA2EtGNVdggfGRGIjSBJazrKZ02Sm7fnw4tkW_aS-xRyvrEK2P8T3HpR1JI8d5hZtYpngpmsbyq5Y93Gi2O1OUDWe0JNELvQCwSFMpSTYyzEKGsRoEXdOuy3DmKQ53LCMaI3Qvr6YBmBj_zVDqM_5Dsslr6zsJ_vX1Ns",
    "gulu_source_res": "eyJwX2luIjoiMWRhNjE1MjEzNDMxNTI4YzJmY2M0M2QwZWM5ZjY0ODFjODgxMjZkN2M0NjlhYjZhZWNlMDRlOTFjZGRlYzJiYSJ9",
    "passport_auth_mix_state": "",# 浏览器中查看
    "bd_ticket_guard_client_data_v2": ""# 浏览器中查看
}
url = "https://www.douyin.com/aweme/v1/web/comment/list/"

def get_time(ctime):
    time_loacl = time.localtime(ctime)
    time_format = time.strftime("%Y-%m-%d ", time_loacl)
    return str(time_format)

def get_json(aweme_id, cursor):
    # query = urllib.parse.urlparse(url).query
    # a_bogus = execjs.compile(open('XB.js').read()).call('sign', query, headers.get('user-agent'))
    # video_url = url + '&X-Bogus' + a_bogus

    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": aweme_id,
        "cursor": cursor,
        "count": "10",
        "item_type": "0",
        "insert_ids": "",
        "whale_cut_token": "",
        "cut_version": "1",
        "rcFT": "",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "12",
        "version_code": "170400",
        "version_name": "17.4.0",
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
        "round_trip_time": "150",
        "webid": "7586653262305838618",
        "uifid": "e3b4cbff814331e10738d4b0ca1195207b8054e7f97d772f5caebc86037fab868c16f1a9324847a7a0162bc606f40ca28ffe7280c865b3555e97f2f981034f1fd9f24fba286f2f4b9a456b10bd675c7d835a93593a9c3d3b27629a3ef2b49d068935a249e026a22ca45b2d84e672cc198d039de603ed76d6a61c55b15c3a0a8d6f3343d0211b1ea09c7e637ddd4b6e78f6430db02208fa8677bd4ee1a27e723c994506f2f1bbe7c35f29d799cf2a8772eb9f6121f34493afae219bfef23a168b",
        "msToken": "",# 批量采集的加密
        "a_bogus": "",# 批量采集的加密，可通过补环境或者及诶
        "fp": "verify_mjh45f7a_TAQK1CHM_6ExF_4Kqf_BW3S_6SKXhZnBVcsr"
    }
    time.sleep(random.randint(1, 5))
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(response.text)
    print(response)

    return response.json()

# 解析数据
def parseData(feed, aweme_id):
    ip_label = feed['ip_label']
    try:
        username = feed['user']['nickname']
    except:
        username = ''
    comment_dit = {
        '用户id': feed['user']['uid'],
        '用户名': username,
        '评论内容': feed.get('text', ' '),
        '评论时间': get_time(feed['create_time']),
        'IP地址': ip_label,
        '点赞数': feed.get('digg_count'),
        '视频id': aweme_id
    }
    print(comment_dit)
    writer.writerow(comment_dit)


def spider_comment(aweme_id):
    cursor = 0
    page = 1
    while True:
        response = get_json(aweme_id, cursor)
        try:
            if response['comments'] is None:
                break
            feeds = response['comments']
            for feed in feeds:
                parseData(feed, aweme_id)
            if response['has_more'] == 0:
                break
            cursor += 20
            page += 1
            if page > 10:
                break
        except Exception as e:
            print(f'爬取失败,报错原因:{e}')
            continue

if __name__ == "__main__":
    header = ['用户id', '用户名', '评论内容', '评论时间', 'IP地址', '点赞数', '视频id']
    f = open('comment.csv', 'a', encoding='utf-8', newline='')
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    df = pd.read_csv('video_data.csv')
    for index, row in df.iterrows():
        spider_comment(row['视频ID'])

