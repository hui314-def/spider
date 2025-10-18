import os
import numpy as np

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
    new_lst=[]
    sort_lst=[]
    for i in lst:
        if '.' not in i:
            print('文件夹内不能包含文件夹！')
            return 
        a=i.split('.')[0]#文件名去除后缀
        a=int(a.split('_')[-1]) #根据文件名提取对应索引，具体情况具体分析
        new_lst.append(a)
    new_lst=np.array(new_lst)
    index=np.argsort(new_lst)#给索引排序
    for i in index:
        sort_lst.append(lst[i])
    with open(name+'.mp4','ab') as w:#将每个文件写入同一个文件内
        for i in sort_lst:
            new_path=os.path.join(path,i)
            with open(new_path,'rb') as r:
                w.write(r.read())
    # 删除原文件
    for i in sort_lst:
        try:
            os.remove(os.path.join(path, i))
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

k='1'
while k=='1':
    main()
    k=input('是否继续合成？(按1以继续)')

print('退出程序')
