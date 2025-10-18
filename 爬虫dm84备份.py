import requests,threading,re
import aiohttp as h
# dm84动漫网

def download_lst(min,max,dic,num):
    for i in range(min,max+1):
        a=f'https://dm84.top/list-{num}-{i}.html'
        main=requests.get(a)
        c=re.compile(r'<a class="title" href="(?P<address>.*?)" title="(?P<name>.*?)">',re.S)
        key=c.finditer(main.text)
        for j in key:
            dic[j.group('name')]=j.group('address')
        main.close()
    
def download_num(url):
    resp=requests.get(url)
    c=re.compile(r'',re.S)
    key=c.finditer(resp.text)



def search(dic):
    search={}
    name=input('请输入你搜索的动漫：')
    for i in dic.keys():
        if name in i:
            search[i]=dic[i]
    print('你搜索出的动漫有：',search)
    key=input('请输入你要下载的动漫：')
    if key in search.keys():
        url='https://dm84.top'+search[key]
        print('你要下载的动漫地址为：',url)
        return url
    else:
        print('没有你要下载的动漫！')

def main():
    num=int(input('请输入你要搜索的动漫：(1.国产动漫 2.日本动漫 3.欧美动漫 4.电影)'))
    dic={}
    a=int(input('请输入你要爬取的页数：'))
    download_lst(1,a//2,dic,num)
    t=threading.Thread(target=download_lst,args=(a//2+1,a,dic,num))
    t.start()
    t.join()
    print('完成！')
    print(dic)
    url=search(dic)
    download_num(url)

main()