import requests,time,json
from lxml import etree
import tkinter as tk
from tkinter import filedialog
import os
from tkinter import ttk
import threading

class BilibiliDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("爬虫b站")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text="视频链接地址:").grid(row=0, column=0, sticky="e", pady=5)
        self.url_entry = ttk.Entry(main_frame, width=45)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky="w", pady=5)

        ttk.Label(main_frame, text="命名:").grid(row=1, column=0, sticky="e", pady=5)
        self.name_entry = ttk.Entry(main_frame, width=45)
        self.name_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

        ttk.Label(main_frame, text="Cookie:").grid(row=2, column=0, sticky="e", pady=5)
        self.cookie_entry = ttk.Entry(main_frame, width=45)
        self.cookie_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        self.cookie_label = ttk.Label(main_frame,text='(非必填项)')
        self.cookie_label.grid(row=2, column=1, columnspan=2, sticky="e", pady=5)
        self.download_video = tk.BooleanVar(value=True)
        self.download_audio = tk.BooleanVar(value=True)
        ttk.Label(main_frame, text="下载选项:").grid(row=3, column=0, sticky="e", pady=5)
        ttk.Checkbutton(main_frame, text="下载视频", variable=self.download_video).grid(row=3, column=1, sticky="w")
        ttk.Checkbutton(main_frame, text="下载音频", variable=self.download_audio).grid(row=3, column=2, sticky="w")

        ttk.Label(main_frame, text="保存路径:").grid(row=4, column=0, sticky="e", pady=5)
        self.save_path = tk.StringVar()
        self.save_entry = ttk.Entry(main_frame, textvariable=self.save_path, width=33)
        self.save_entry.grid(row=4, column=1, sticky="w")
        ttk.Button(main_frame, text="选择", command=self.choose_path).grid(row=4, column=2, sticky="w")

        ttk.Separator(main_frame, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky="ew", pady=10)

        self.download_btn = ttk.Button(main_frame, text="下载", command=self.start_download_thread)
        self.download_btn.grid(row=6, column=0, columnspan=3, pady=5)

        self.status = ttk.Label(main_frame, text="", foreground="blue")
        self.status.grid(row=7, column=0, columnspan=3, pady=5)

        ttk.Label(main_frame, text="下载信息:").grid(row=8, column=0, sticky="nw")
        self.info = tk.Text(main_frame, height=7, width=55, font=("Consolas", 10))
        self.info.grid(row=8, column=1, columnspan=2, sticky="w")

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path.set(path)

    def start_download_thread(self):#启动多线程下载，防止界面卡顿
        t = threading.Thread(target=self.download)
        t.daemon = True
        t.start()

    def download(self):
        url = self.url_entry.get()
        name = self.name_entry.get()
        cookie = self.cookie_entry.get()
        save_dir = self.save_path.get()
        self.status.config(text="正在下载...")
        self.info.delete(1.0, tk.END)
        self.root.update()
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
                'Cookie': cookie
            }
            res = requests.get(url, headers=header)
            tree = etree.HTML(res.text)
            n = str(tree.xpath('/html/head/script/text()')[3]).replace('window.__playinfo__=', '')
            j = json.loads(n)
            video = j["data"]["dash"]["video"][0]
            urls_video = [video.get("baseUrl"), video.get("base_url"), video.get("backupUrl"), video.get("backup_url")]
            audio = j["data"]["dash"]["audio"][0]
            urls_audio = [audio.get("baseUrl"), audio.get("base_url"), audio.get("backupUrl"), audio.get("backup_url")]
            headers = {
                'User-Agent': header['User-Agent'],
                'Referer': url,
                'Cookie': cookie
            }
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            if self.download_video.get():
                for i in urls_video:
                    if i:
                        self.status.config(text="正在下载视频...")
                        self.root.update()
                        x1 = time.time()
                        res_video = requests.get(i, headers=headers)
                        video_path = os.path.join(save_dir, name + '.mp4')
                        with open(video_path, 'wb') as f:
                            f.write(res_video.content)
                        res_video.close()
                        x2 = time.time()
                        size = os.path.getsize(video_path) / 1024 / 1024
                        self.info.insert(tk.END, f"视频下载完成: {video_path}\n用时: {x2-x1:.2f}秒\n文件大小: {size:.2f}MB\n")
                        break
                else:
                    self.info.insert(tk.END, "视频下载失败\n")
            if self.download_audio.get():
                for i in urls_audio:
                    if i:
                        self.status.config(text="正在下载音频...")
                        self.root.update()
                        y1 = time.time()
                        res_audio = requests.get(i, headers=headers)
                        audio_path = os.path.join(save_dir, name + '.m4a')
                        with open(audio_path, 'wb') as f:
                            f.write(res_audio.content)
                        res_audio.close()
                        y2 = time.time()
                        size = os.path.getsize(audio_path) / 1024 / 1024
                        self.info.insert(tk.END, f"音频下载完成: {audio_path}\n用时: {y2-y1:.2f}秒\n文件大小: {size:.2f}MB\n")
                        break
                else:
                    self.info.insert(tk.END, "音频下载失败\n")
            self.status.config(text="下载完成")
        except Exception as e:
            self.status.config(text="下载出错")
            self.info.insert(tk.END, f"错误: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BilibiliDownloaderGUI(root)
    root.mainloop()


'''以下是自己手搓的代码
url=input('视频链接地址：')
name=input('命名:')
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
}
res=requests.get(url,headers=header)

tree=etree.HTML(res.text)

n=str(tree.xpath('/html/head/script/text()')[3]).replace('window.__playinfo__=','')
j=json.loads(n)
video=j["data"]["dash"]["video"][0]
urls_video=[video["baseUrl"],video["base_url"],video["backupUrl"],video["backup_url"]]
audio=j["data"]["dash"]["audio"][0]
urls_audio=[audio["baseUrl"],audio["base_url"],audio["backupUrl"],audio["backup_url"]]


cookie=input('cookie:')
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'Referer':url,
    'Cookie':cookie
}
for i in urls_video:
    if i:
        print('正在下载视频……')
        x1=time.time()
        res_video=requests.get(i,headers=headers)
        with open(name+'.mp4','wb') as f:
            f.write(res_video.content)
        res_video.close()
        x2=time.time()
        print('视频下载完成！用时:',x2-x1,'秒')
        break
else:
    print('视频下载失败')

for i in urls_audio:
    if i:
        print('正在下载音频……')
        y1=time.time()
        res_audio=requests.get(i,headers=headers)
        with open(name+'.m4a','wb') as f:
            f.write(res_audio.content)
        res_audio.close()
        y2=time.time()
        print('音频下载完成！用时:',y2-y1,'秒')
        break

else:
    print('音频下载失败')'''