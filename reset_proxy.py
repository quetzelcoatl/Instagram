import ast
import datetime
import json
import os
import threading
import time

import requests


def reset_proxy(proxy, reset_proxy_num, proxy_code):
    headers = {
        'Authorization': 'Token 7e900b9e6e0d93df5fc975009937d0f1f92d5658',
    }
    IP = proxy.split('@')
    IP = IP[1].split(':')
    print("Selected Proxy : ", proxy)

    print("Resetting Proxy : ", IP[0])
    print("Resetting Proxy Index : ", IP[1])
    # Checking IP before Reset
    """q = "curl --proxy {} https://api.myip.com ".format(proxy)
    output = os.system(q)"""

    status_code = 0
    while status_code != 200:
        ##req = "http://173.92.252.25/api/change_ip?index={}".format(proxy_code[reset_proxy_num])
        #req = "http://{}/api/change_ip?index={}".format(IP[0], IP[1][-1])
        req = f"http://{proxy_code[proxy]}"
        response = requests.get(req, headers=headers)
        print(response.text)
        print("Status Code", response.status_code)
        print("JSON Response ", response.json())
        status_code = response.status_code
        if status_code == 200:
            break
        time.sleep(30)
    time.sleep(20)

    # Checking IP after Reset
    q = "curl --proxy {} https://api.myip.com ".format(proxy)
    output = os.system(q)

"""ppp = {'Rjenkins313:Audit313@5.161.106.85:10001': '5.161.106.85:10550/api/change_ip?index=1', 'Rjenkins313:Audit313@5.161.106.85:10002': '5.161.106.85:10550/api/change_ip?index=2', 'Rjenkins313:Audit313@5.161.106.85:10003': '5.161.106.85:10550/api/change_ip?index=3', 'Rjenkins313:Audit313@5.161.106.85:10004': '5.161.106.85:10550/api/change_ip?index=4', 'Rjenkins313:Audit313@5.161.106.85:10005': '5.161.106.85:10550/api/change_ip?index=5'}
reset_proxy(list(ppp.keys())[1], 0, ppp)"""
#OLD SAFE
"""    headers = {
            'Authorization': 'Token 7e900b9e6e0d93df5fc975009937d0f1f92d5658',
        }
    print("Resetting index : ",reset_proxy_num)
    status_code = 0
    while status_code != 200:
        ##req = "http://173.92.252.25/api/change_ip?index={}".format(proxy_code[reset_proxy_num])
        req = "http://70.142.219.240/api/change_ip?index={}".format(proxy_code[reset_proxy_num])
        response = requests.get(req, headers=headers)
        print(response.text)
        print("Status Code", response.status_code)
        print("JSON Response ", response.json())
        status_code = response.status_code
        if status_code == 200:
            break
        time.sleep(30)
    time.sleep(5)"""


#FOR ILLUSORY
"""data = {
        "apiKey": "SCON05X39T02P79jIs1XGF870AyYN5pyi1JVv7h21x",
        "authEmail": "rjenkins313@gmail.com",
        "proxy": proxy_code[reset_proxy_num],
    }

    url = "https://api.illusory.io/api:Oj9wVgoa/changeIp"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)

    print("Status Code", response.status_code)
    print("JSON Response ", response.json())

    if str(response.json) == "Unsuccessful. Please wait at least 60 seconds before changing IP.":
        time.sleep(30)
        url = "https://api.illusory.io/api:Oj9wVgoa/changeIp"
        headers = {"Content-Type": "application/json"}
        data = {
            "apiKey": "SCON05X39T02P79jIs1XGF870AyYN5pyi1JVv7h21x",
            "authEmail": "rjenkins313@gmail.com",
            "proxy": proxy_code[reset_proxy_num],
        }
        response = requests.post(url, headers=headers, json=data)
        print("Status Code 2", response.status_code)
        print("JSON Response 2", response.json())

    output = 35
    print("Resetting proxy")
    time.sleep(30)
    while output == 35 or output == 7:
        print(proxy)
        q = "curl --proxy {}  ".format(proxy)
        output = os.system(q)
        print(output)

    print("Succesfully Reset Proxy")"""