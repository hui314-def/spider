import os
'''合并视频切片，适用于文件夹内的文件按照顺序命名，如1.ts，2.ts，3.ts……'''

def main(delete_original=False):
    try:
        path=input('输入要合成视频的文件夹路径：')
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

k='1'
while k=='1':
    main(True) #合成后删除原文件
    k=input('是否继续合成？(按1以继续)')

print('退出程序')
