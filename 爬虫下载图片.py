import requests
import re

def downloadimage(url):#下载图片
    list=re.split(r'/',url)
    name=list[-1]
    resp=requests.get(url)
    with open(name,mode='wb') as f:
        f.write(resp.content)
        print('下载完成')

downloadimage('https://p2.ssl.qhimgs1.com/t01a4ef511318b8d0e7.png')


