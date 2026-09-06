from pprint import pprint

import execjs
import requests

headers = {
    "authority": "api.qimai.cn",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt-BR;q=0.5,pt;q=0.4",
    "cache-control": "no-cache",
    "dnt": "1",
    "origin": "https://www.qimai.cn",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}
cookies = {
    "gr_user_id": "2be94f90-dfe2-4ddf-a8f4-0cbecfa02e5e",
    "Hm_lvt_ff3eefaf44c797b33945945d0de0e370": "1681785424,1682245115,1682260278",
    "PHPSESSID": "mihdtl727nh156rkj8rikr44lb",
    "qm_check": "A1sdRUIQChtxen8pI0dANi8zcX5zHBl+YnEhLyZIPxw8WkVRVRl3YGBFV1FeSFkuXBcaAEEABAhVVFZRSVBacV5AVVpEB3xUV0ceCyZPagcSQEpvAWdVSkcsSz1LBB4QHBtTXF0GDUVSWklWBRsCHAkcBBoY",
    "ada35577182650f1_gr_session_id": "c8bf2bc6-94a7-4e62-8e47-9a9b6300e6c7",
    "ada35577182650f1_gr_session_id_sent_vst": "c8bf2bc6-94a7-4e62-8e47-9a9b6300e6c7",
    "tgw_l7_route": "d09474674af82c17375cfcdd775c0c28",
    "aso_ucenter": "4aebF5JGRFFZCT7s8kf5ATFP8wY8P573QJbhp6ctfkUpOF%2BrXdlGVklVEUiecWyjcvA",
    "USERINFO": "gl9a8RkIkJbaiXCBx1%2BDQhVcJUyRzee6swytGjrffO%2FUcPR3Sm9TnUKYTcLaUoGnAZ2chfqVuP38HUHwVlZD%2FPDOCraZ1Wwp%2BN2BjpXv3gzAOEN8lLuj7Bz0mHMalXnSbA%2Bimklzwo8dobWaJkXXnw%3D%3D",
    "ada35577182650f1_gr_last_sent_sid_with_cs1": "c8bf2bc6-94a7-4e62-8e47-9a9b6300e6c7",
    "ada35577182650f1_gr_last_sent_cs1": "qm20144047089",
    "AUTHKEY": "yJ%2FkP5mfdKnUO1kKvrMF4EPue1bFLUaiRjqo5ujzkvvKXUuMhcPeiH4c7u52kRnv95B%2FoqNkS7NLj8O%2FiAwkLNvsrc3XvkqRrVRO0qbNRDZgK1jO4NVyjw%3D%3D",
    "synct": "1701440477.236",
    "syncd": "234",
    "ada35577182650f1_gr_cs1": "qm20144047089"
}
url = "https://api.qimai.cn/rank/index"
cell = execjs.compile(open('util\\analysis.js', encoding='utf-8').read())
params = {"brand": "free", "device": "iphone", "country": "cn", "genre": "5000", "date": "2023-04-23", "page": "1",
          "is_rank_index": "1", 'snapshot': '21:15:03'}
# 翻页查询修改page,爬取不同网页修改params
key = list(params.values())
print(key)
analysis = cell.call('lzl', key, '/rank/index')
params['analysis'] = analysis
response = requests.get(url, headers=headers, cookies=cookies, params=params)
# print(response.url)
pprint(response.json())

