import requests,re
import aiohttp
import asyncio as asy

base_url = 'https://dm84.top' # dm84动漫网

async def download_lst(url,dic,session):
    c = re.compile(r'<a class="title" href="(?P<address>.*?)" title="(?P<name>.*?)">', re.S)
    async with session.get(url) as resp:
        key = c.finditer(await resp.text()) # 提取网页文字要调用方法text()
        for j in key:
            dic[j.group('name')] = j.group('address')

def episode_num(url):
    resp = requests.get(url)
    c1 = re.compile(r'<ul class="play_list current"><li><a href="/p/.*?.html">(?P<num1>\d{1,4})', re.S)
    key = c1.finditer(resp.text)
    for i in key:
        n1 = int(i.group('num1')) # 首位标签可能提取到的数字为1
    c2 = re.compile(r'<li><a href="/p/.*?.html">(?P<num2>\d{1,4})</a></li></ul></div>', re.S)
    key = c2.finditer(resp.text)
    for i in key:
        n2 = int(i.group('num2')) # 找末尾标签
    if n1 > n2:
        n = n1
    else:
        n = n2
    print(f'你选择的动漫一共有{n}集')
    return n

def search(dic):
    search = {}
    name = input('请输入你搜索的动漫：')
    for i in dic.keys():
        if name in i: # 关键字检索
            search[i] = dic[i] # 存入搜索出的内容
    print('你搜索出的动漫有：', search)
    key = input('请输入你要看的动漫：')
    if key in search.keys(): # 找到对应的动漫及其地址
        url = base_url + search[key]
        print('你要看的动漫地址为：', url)
        return url
    else:
        print('没有你要看的动漫！')

async def main():
    num = int(input('请输入你要搜索的动漫：(1.国产动漫 2.日本动漫 3.欧美动漫 4.电影)'))
    a = int(input('请输入你要爬取的页数：'))
    urls = []
    dic = {}
    for i in range(1, a + 1):
        urls.append(f'{base_url}/list-{num}-{i}.html')
    async with aiohttp.ClientSession() as session: # 开启异步协程会话
        tasks = []
        for url in urls:
            task = asy.create_task(download_lst(url, dic, session))
            tasks.append(task) # 添加每个任务
        await asy.wait(tasks)

    print(dic)
    url = search(dic)
    sum = episode_num(url)
    num = int(input(f'请问你要下载哪一集？(输入数字,输入0默认下载所有集)：'))
    if num > 0 and num <= sum:
        temp = url.split('.')[0]
        n = temp.split('/')[-1] # 分割出视频标号
        url = f'{base_url}/p/{n}-1-{num}.html' # 合成视频地址
        print(url)
    elif num == 0:
        print('开始下载全部集数')
    else:
        print('输入有误！')
        return

asy.run(main())
