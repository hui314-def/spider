import requests,aiohttp,aiofiles,os,time
import asyncio as asy

num=0 # 全局变量
def progress_bar(current, total, bar_length=50): # 下载进度条
    percent = current / total
    arrow = '█' * int(bar_length * percent)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'\r下载进度: [{arrow}{spaces}] {current}/{total}={current/total*100:.1f}%', end='', flush=True)

async def download(url,name,session,file): # 异步调用下载函数
    global num,sum
    async with session.get(url) as resp:
        async with aiofiles.open(f'{file}/{name}','wb') as f:
            await f.write(await resp.content.read())
    num+=1
    progress_bar(num,sum)

async def main():
    global sum
    file=input('创建的文件夹命名为：')
    os.makedirs(file,exist_ok=True)
    url_m3u8=input('爬取的m3u8地址：')
    x1=time.time()
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'}
    resp=requests.get(url_m3u8,headers=headers)
    with open(file+'.m3u8','wb') as f:
        f.write(resp.content)
    tasks=[]
    timeout=aiohttp.ClientTimeout(total=9999) # 延长会话时间（原默认300s）
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with aiofiles.open(file+'.m3u8','r') as f:
            async for line in f:
                if line.startswith('#'):
                    continue
                line=line.strip()
                a=url_m3u8.split('video_') # 特殊情况特殊分析
                url=a[0]+line # 拼出真实下载路径
                task=asy.create_task(download(url,line,session,file)) # 创建任务
                tasks.append(task) # 添加下载任务
            sum=len(tasks)
            await asy.wait(tasks)
    print(f'\n{file} 全部下载完毕！')
    x2=time.time()
    print(f'下载用时：{x2-x1:.2f}秒')
    
k='1'
while k=='1':
    asy.run(main())
    k=input('是否继续下载？(是则输入1，否则输入其他任意)')
    num=0

print('退出程序')
