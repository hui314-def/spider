import requests
from lxml import etree
header={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}
num=0
url=input('书籍网址：')
base_url=url.split('.com')[0]+'.com'
name=input('命名：')
resp=requests.get(url,headers=header)
t=etree.HTML(resp.text)
elements=t.xpath('/html/body/div[1]/div[3]/div[3]/div[2]/ul/li/a/@href')
with open(name+'.txt','a',encoding='utf-8') as f:
    for i in elements:
        url_0=base_url+i
        resp_0=requests.get(url_0,headers=header)
        n=etree.HTML(resp_0.text)
        e=n.xpath('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/p/text()')
        for j in e:
            f.write(j)
        num+=1
        print(f'\r下载进度：{num}/{len(elements)}',end='')

print('下载完成！')