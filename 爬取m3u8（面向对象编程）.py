import os
import time
import asyncio
import aiohttp
import aiofiles
import requests

class M3U8Downloader:
    """M3U8 视频下载器，支持异步并发下载 TS 片段，并提供下载进度显示和交互式输入功能，需要提供m3u8文件的URL和存储文件夹名称。"""

    def __init__(self, headers=None):
        """初始化下载器，设置请求头和内部计数器"""
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
        }
        self.total_segments = 0      # 总片段数
        self.downloaded = 0          # 已下载片段数
        self.index = 1               # 当前下载片段索引

    @staticmethod
    def get_base_url(m3u8_url: str) -> str:
        """
        根据 m3u8 文件的 URL 提取基础路径（用于拼接 TS 文件 URL）
        实际使用时可能需要根据具体 URL 结构调整分割关键字
        """
        return m3u8_url

    def progress_bar(self, current: int, total: int, bar_length: int = 50) -> None:
        """显示下载进度条"""
        percent = current / total if total > 0 else 0
        arrow = '█' * int(bar_length * percent)
        spaces = ' ' * (bar_length - len(arrow))
        print(f'\r下载进度: [{arrow}{spaces}] {current}/{total} = {percent * 100:.1f}%',
              end='', flush=True)

    async def download_segment(self, url: str, filename: str, session: aiohttp.ClientSession,
                               folder: str) -> None:
        """异步下载单个 TS 片段并保存到本地文件"""
        async with session.get(url, headers=self.headers) as resp:
            async with aiofiles.open(os.path.join(folder, filename), 'wb') as f:
                await f.write(await resp.content.read())

        self.downloaded += 1
        self.progress_bar(self.downloaded, self.total_segments)

    async def download_m3u8(self, m3u8_url: str, folder: str) -> None:
        """下载整个 M3U8 视频流：
        1. 创建存放 TS 文件的文件夹
        2. 下载 M3U8 索引文件并保存
        3. 解析索引文件，并发下载所有 TS 片段"""
        if os.path.exists(folder):
            print(f"文件夹 '{folder}' 已存在，是否继续使用？(是则输入1，否则输入其他任意)")
            choice = input()
            if choice != '1':
                return
        os.makedirs(folder, exist_ok=True)

        # 下载 M3U8 索引文件
        resp = requests.get(m3u8_url, headers=self.headers)
        m3u8_path = f"{folder}.m3u8"
        with open(m3u8_path, 'wb') as f:
            f.write(resp.content)

        # 准备异步任务
        tasks = []
        timeout = aiohttp.ClientTimeout(total=9999)  # 延长总超时时间

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with aiofiles.open(m3u8_path, 'r') as f:
                async for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # 拼接 TS 文件的完整 URL
                    base = self.get_base_url(m3u8_url)
                    ts_url = base + line
                    task = asyncio.create_task(
                        self.download_segment(ts_url, f"{self.index}.ts", session, folder) # 文件命名为 1.ts, 2.ts, ...
                    )
                    tasks.append(task)
                    self.index += 1

            self.total_segments = len(tasks)
            if self.total_segments == 0:
                print("未找到任何 TS 片段，请检查 M3U8 文件格式。")
                return

            await asyncio.wait(tasks)

        print(f"\n文件夹 '{folder}' 中的全部片段下载完毕！")

    async def run_interactive(self) -> None:
        """交互式运行：循环接收用户输入，下载多个 M3U8 视频"""
        while True:
            folder = input("创建的文件夹命名为：").strip()
            if not folder:
                print("文件夹名不能为空，请重新输入。")
                continue

            m3u8_url = input("爬取的 M3U8 地址：").strip()
            if not m3u8_url:
                print("URL 不能为空，请重新输入。")
                continue

            start_time = time.time()
            await self.download_m3u8(m3u8_url, folder)
            elapsed = time.time() - start_time
            print(f"下载用时：{elapsed:.2f} 秒")

            again = input("是否继续下载？(是则输入1，否则输入其他任意)：").strip()
            if again != '1':
                break
            self.downloaded = 0
            self.index = 1

        print("退出程序")


if __name__ == '__main__':
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'Referer': 'https://cn.pornhub.com/',
    }
    downloader = M3U8Downloader(headers)
    asyncio.run(downloader.run_interactive())