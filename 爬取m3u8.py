import requests,aiohttp,aiofiles,os
import asyncio as asy
import time 

# 全局变量
sum=0; num=0; headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'}

def progress_bar(current, total, bar_length=50): # 下载进度条
    percent = current / total
    arrow = '█' * int(bar_length * percent)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'\r下载进度: [{arrow}{spaces}] {current}/{total}={current/total*100:.1f}%', end='', flush=True)

async def download(url,name,session,file):
    async with session.get(url,headers=headers) as resp:
        async with aiofiles.open(f'{file}/{name}','wb') as f:
            await f.write(await resp.content.read())
    global num, sum
    num+=1
    progress_bar(num,sum)

async def main():
    global sum
    file = input('创建的文件夹命名为：')
    os.mkdir(file)
    url_m3u8 = input('爬取的m3u8地址：')
    x1 = time.time()
    resp = requests.get(url_m3u8,headers=headers)
    with open(file+'m3u8.txt','wb') as f:
        f.write(resp.content)
    tasks = [] # 任务列表
    timeout = aiohttp.ClientTimeout(total=9999) # 延长会话时间（原默认300s）
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with aiofiles.open(file+'m3u8.txt','r') as f:
            async for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()
                a = url_m3u8.split('mixed') # 特殊情况特殊分析
                url = a[0]+line # 拼出真实下载路径
                task = asy.create_task(download(url,line,session,file)) # 创建任务
                tasks.append(task)
            sum = len(tasks)
            await asy.wait(tasks)
    print(f'\n{file} 全部下载完毕！')
    x2=time.time()
    print(f'下载用时：{x2-x1:.2f}秒')
    
if __name__ == '__main__':
    k='1'
    while k=='1':
        asy.run(main())
        k=input('是否继续下载？(是则输入1，否则输入其他任意)')

    print('退出程序')