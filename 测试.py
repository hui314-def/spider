import urllib.request
import requests
import time
import random
import os
import re

# 设置日志文件路径
log_file_path = 'log.txt'

# 第一个post请求的URL
post_URL = 'http://10.100.255.2/eportal/InterFace.do?method=login'
# 第二个get请求的URL（浏览器可访问的url）
get_URL = 'http://10.100.255.2/eportal/success.jsp?userIndex=63360363366306533343048342464646&keepaliveInterval=0'

while True:
    print("自动联网脚本运行中...")
    try:
        # 请求校园网url（添加超时防止阻塞）
        response = urllib.request.urlopen(get_URL, timeout=10)
        html = response.read()
    except Exception as e:
        print(f"网络请求异常: {e}")
        html = b''  # 防止html未定义

    # 获取title元素内容
    res = re.findall('<title>(.*)</title>', html.decode(encoding="GBK", errors="ignore"))  # 使用errors="ignore"避免解码失败
    print('res:', res)
    title = ''
    if len(res) == 0:
        print(f"访问 {get_URL} 可能未连接到校园网！")
    else:
        title = res[res[0]]

    # 根据title判断登录状态
    if title == '登录成功':
        print('当前状态为：已登录！')
        # 弹出Windows通知
        # try:
        #     toaster.show_notification(
        #         "校园网状态",
        #         "&#9989; 已成功连接到校园网！",
        #         duration=5,
        #         icon_path="school.ico",  # 可替换为图标路径如 "school.ico"
        #         threaded=True
        #     )
        # except Exception as e:
        #     print(f"通知发送失败: {e}")
    else:
        print('当前状态为：未登录！')
        # 设置post请求头和数据
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "691",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "EPORTAL_COOKIE_SERVER=; EPORTAL_COOKIE_DOMAIN=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_USERNAME=SCXY15182972294; EPORTAL_COOKIE_NEWV=true; EPORTAL_COOKIE_SERVER_NAME=;",
            "Host": "XXXX",  #根据自己的浏览器配置项配置
            "Origin": "XXXXX",  #根据自己的浏览器配置项配置
            "Referer": "XXXXX", #根据自己的浏览器配置项配置
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }
        data = {
            "userId": 'XXXXX',   #根据自己的浏览器配置项配置
            "password": 'XXXXX',  #根据自己的浏览器配置项配置
            "queryString": 'XXXXX',  #根据自己的浏览器配置项配置
            "passwordEncrypt": 'true',
            "operatorPwd": '',
            "operatorUserId": '',
            "validcode": '',
            "service": '',
        }

        # 发送登录请求
        try:
            post_response = requests.post(post_URL, data=data, headers=header, timeout=15)
            print(f"POST请求状态码: {post_response.status_code}")
            get_response = requests.get(get_URL, timeout=15)
            print(f"GET请求状态码: {get_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")

    # 日志记录（添加异常处理）
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 状态: {'已登录' if title == '登录成功' else '未登录'}\n")
            if os.path.getsize(log_file_path) > 1024:
                log_file.seek(0)
                log_file.truncate()  # 更安全的清空方式
    except IOError as e:
        print(f"日志写入失败: {e}")

    # 随机休眠（1小时±100秒）
    delay = 3600 + random.uniform(-100, 100)
    print(f"下次检测将在 {int(delay)} 秒后...\n")
    time.sleep(delay)
