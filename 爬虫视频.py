import requests,os

url='https://v9.tlkqc.com/wjv9/202504/19/wxPHfv8iQG81/video/1000k_720/hls/index.m3u8'
resp=requests.get(url)
with open('1.txt','w',encoding='utf-8') as f:
    f.write(resp.text)
print('m3u8 下载完成')
with open('1.txt','r',encoding='utf-8') as f:
    lines=f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        line=line.strip()
        resp=requests.get(line)
        name=line.split('/')[-1]
        with open('sp/'+name,'wb') as f:
            f.write(resp.content)
        print(name,'下载完成')




'''with open('sp.ts','ab') as f:
    dir=os.listdir('sp')
    for i in dir:
        with open('sp/'+i,'rb') as r:
            f.write(r.read())'''


