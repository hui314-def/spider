import os

def main():
    try:
        path=input('输入要合成视频的文件夹路径：')
        lst=os.listdir(path)
    except:
        print('文件不存在！')
        return 
    for file in lst:
        if os.path.getsize(os.path.join(path,file))==0:
            print('注意：文件名',file,'的大小为0')
    name=path #可修改名称
    if os.path.isfile(name+'.mp4'):
        print('该文件已存在')
        return 
    sort_lst=[]
    with open(name+'m3u8.txt','r',encoding='utf-8') as f:#利用m3u8的顺序依次存储要合成的文件
        for line in f:
            if line.startswith('#'):
                continue
            line=line.strip()
            sort_lst.append(line)

    with open(name+'.mp4','ab') as w:#将每个文件写入同一个文件内
        for i in sort_lst:
            new_path=os.path.join(path,i)
            try:
                with open(new_path,'rb') as r:
                    w.write(r.read())
            except:
                print(i,'不存在！')
    '''# 删除原文件
    for i in sort_lst:
        try:
            os.remove(os.path.join(path, i))
        except Exception as e:
            print(f"删除文件 {i} 时出错: {e}")
    try:
        os.rmdir(path)
    except Exception as e:
        print(f"删除文件夹 {path} 时出错: {e}")

    print('完成！自动删除原文件')'''

k='1'
while k=='1':
    main()
    k=int(input('是否继续合成？(按1以继续)'))
print('退出程序')