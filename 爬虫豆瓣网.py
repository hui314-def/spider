import requests
from lxml import html
import json

url = 'https://movie.douban.com/top250?start=0'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}
resp = requests.get(url, headers=header)
tree = html.fromstring(resp.text)
addresses = tree.xpath('//li/div/div/div/a/@href')
names = tree.xpath('//li/div/div/div/a/span[1]/text()')
scores = tree.xpath('//li/div/div/div/div/span[@class="rating_num"]/text()')
sum = []


for rank, (address, name, score) in enumerate(zip(addresses, names, scores), start=1):
    response = requests.get(address, headers=header)
    # with open('movie_detail.html', 'r', encoding='utf-8') as f:
    #     response_text = f.read()
    tree = html.fromstring(response.text)
    directors = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[2]/a/text()')
    if len(directors) == 1:
        directors = directors[0]
    screenwriters = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]/span[2]/a/text()')
    if len(screenwriters) == 1:
        screenwriters = screenwriters[0]
    actors = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[3]/span[@class="attrs"]/a/text()') #

    types = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[@property="v:genre"]/text()')
    if len(types) == 1:
        types = types[0]
    release_date = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[@property="v:initialReleaseDate"]/text()')
    if len(release_date) == 1:
        release_date = release_date[0]
    length = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[@property="v:runtime"]/text()')[0] 
    people_num = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
    introduction = tree.xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[3]/div/span[1]/span/text()')[0].strip()

    dic = {
        '排名': rank,
        '名称': name,
        '地址': address,
        '评分': score,
        '导演': directors,
        '编剧': screenwriters,
        '主演': actors,
        '类型': types,
        '上映日期': release_date,
        '片长': length,
        '评价人数': people_num,
        '简介': introduction
    }
    sum.append(dic)

# 整齐打印
for item in sum:
    print(json.dumps(item, ensure_ascii=False, indent=2))


# 保存为json文件
with open('douban_movies.json', 'w', encoding='utf-8') as f:
    json.dump(sum, f, ensure_ascii=False, indent=2)