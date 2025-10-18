import re
import requests
url='https://axutongxue.com/'
b=requests.get(url).text
c=re.compile(r'.*?<li><i class=".*?"></i><a HREF="(?P<address>.*?)">(?P<name>.*?)</a>',re.S)
key=c.finditer(b)
with open('阿虚同学收藏的网址.txt',mode='w',encoding='utf-8') as f:
    for i in key:
        f.write('名字：'+i.group('name')+'\n')
        f.write('地址：'+i.group('address')+'\n')
    
