import requests,aiohttp,aiofiles,os
import asyncio as asy
import time
import subprocess

# 全局变量
sum=0; num=0
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
    'Referer': 'https://cn.pornhub.com/',
}

def progress_bar(current, total, bar_length=50): # 下载进度条
    percent = current / total
    arrow = '█' * int(bar_length * percent)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'\r下载进度: [{arrow}{spaces}] {current}/{total}={current/total*100:.1f}%', end='', flush=True)

async def download(url,name,session,file):
    async with session.get(url,headers=headers) as resp:
        async with aiofiles.open(f'{file}/{name}.ts','wb') as f:
            await f.write(await resp.content.read())
    global num, sum
    num += 1
    progress_bar(num,sum)

async def main():
    global sum
    index = 1
    file = input('创建的文件夹命名为：')
    os.makedirs(file, exist_ok=True)
    url_m3u8 = input('爬取的原m3u8地址：')
    base_url = url_m3u8.rsplit('/',1)[0]+'/' # 获取m3u8所在目录的URL
    x1 = time.time()
    with requests.Session() as req_session:
        resp = req_session.get(url_m3u8, headers=headers)
        for line in resp.text.splitlines():
            if line.startswith('#'):
                continue
            line = line.strip()
            url_m3u8 = base_url + line # 拼出真实下载路径
            break

        resp = req_session.get(url_m3u8, headers=headers)
        with open(file + '.m3u8', 'wb') as f:
            f.write(resp.content)
    tasks = [] # 任务列表
    timeout = aiohttp.ClientTimeout(total=9999) # 延长会话时间（原默认300s）
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with aiofiles.open(file+'.m3u8','r') as f:
            async for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()
                url = base_url+line # 拼出真实下载路径
                task = asy.create_task(download(url,index,session,file)) # 创建任务
                tasks.append(task)
                index += 1
            sum = len(tasks)
            await asy.wait(tasks)
    print(f'\n{file} 全部下载完毕！')
    x2 = time.time()
    print(f'下载用时：{x2-x1:.2f}秒')
    return file
    

def merge_ts_files(path, delete_original=False):
    try:
        lst=os.listdir(path)
    except:
        print('文件不存在！')
        return
    
    for file in lst:
        if os.path.getsize(os.path.join(path,file))==0:
            print('警告：文件名',file,'的大小为0')
    
    # 检查是否有缺失的文件
    i = 1
    while os.path.isfile(os.path.join(path, f'{i}.ts')):
        i += 1
    expected_count = i - 1
    
    missing_files = []
    for i in range(1, expected_count + 1):
        if not os.path.isfile(os.path.join(path, f'{i}.ts')):
            missing_files.append(i)
    
    if missing_files:
        print(f'警告：检测到缺失的文件: {missing_files}')
    
    name=path #可修改名称
    if os.path.isfile(name+'.mp4'):
        print('该文件已存在，是否覆盖？(是则输入1，否则输入其他任意)')
        choice = input()
        if choice != '1':
            return

    with open(name+'.mp4','ab') as w:#将每个文件写入同一个文件内
        for i in range(len(lst)):
            new_path=os.path.join(path,f'{i+1}.ts') #根据文件命名规则修改
            with open(new_path,'rb') as r:
                w.write(r.read())
    # 删除原文件
    if delete_original:
        for i in range(len(lst)):
            try:
                os.remove(os.path.join(path, f'{i+1}.ts')) #根据文件命名规则修改
            except Exception as e:
                print(f"删除文件 {i} 时出错: {e}")
        try:
            os.rmdir(path)
        except Exception as e:
            print(f"删除文件夹 {path} 时出错: {e}")
        # 删除m3u8文件
        try:
            os.remove(name+'.m3u8')
        except Exception as e:
            print(f"删除m3u8文件 {path} 时出错: {e}")
        print('完成！成功自动删除原文件')


if __name__ == '__main__':
    k = '1'
    while k == '1':
        file = asy.run(main())
        merge_ts_files(file, delete_original=True)
        subprocess.Popen(['start', f'{file}.mp4'], shell=True)
        k = input('是否继续下载？(是则输入1，否则输入其他任意)')
        num = 0

    print('退出程序')

