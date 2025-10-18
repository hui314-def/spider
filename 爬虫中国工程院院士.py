'''
import requests,os,re

path='中国工程院院士'
if not os.path.exists(path):#创建文件夹
    os.mkdir(path)

for i in range(1,10):
    url_0='https://www.cae.cn/'
    url=f'https://www.cae.cn/cae/html/main/col53/column_53_xb{i}.html'#分不同学部抓取
    resp_0=requests.get(url)#请求一个学部的网站
    key1=re.compile(r'<div class="ysmd_bt clearfix">(?P<department>.*?)</div>',re.S)
    department=key1.findall(resp_0.text)[0]#提取学部名称
    new_path=os.path.join(path,department)
    os.mkdir(new_path)#新建学部文件夹
    key2=re.compile(r'<li class="name_list"><a href="(?P<address>.*?)" target="_blank">(?P<name>.*?)</a></li>',re.S)
    text=key2.finditer(resp_0.text)#提取院士姓名和链接地址
    key3=re.compile(r'<p>&ensp;&ensp;&ensp;&ensp;(?P<text1>.*?)</p><p>&nbsp;</p><p>&ensp;&ensp;&ensp;&ensp;(?P<text2>.*?)</p>',re.S)
    key4=re.compile(r'<div class="info_img">.*?<img src="(?P<img>.*?)"',re.S)

    for i in text:
        resp=requests.get(url_0+i.group('address'))
        text2=key3.finditer(resp.text)#获取简介
        count=1#计数重名院士

        for j in text2:
            file_path = os.path.join(new_path, i.group('name') + '.txt')
            if os.path.exists(file_path):#如果存在院士重名简介
                count += 1
                file_name = i.group('name') + f'_{count}'#换一个文件名保存
                file_path = os.path.join(new_path, file_name + '.txt')
                with open(file_path,'w',encoding='utf-8') as t:#写入简介
                    t.write(j.group('text1'))
                    t.write(j.group('text2'))
                print(file_name,'的简介下载完成')#下载完成的日志
            else:
                count=1
                with open(file_path,'w',encoding='utf-8') as t:
                    t.write(j.group('text1'))
                    t.write(j.group('text2'))
                print(i.group('name'),'的简介下载完成')
        image_address=key4.finditer(resp.text)#获取图片地址
        count=1

        for k in image_address:
            resp1=requests.get(url_0+k.group('img'))#获取照片
            img_filepath = os.path.join(new_path, i.group('name') + '.jpg')
            if os.path.exists(img_filepath):#如果存在院士重名图片
                count += 1
                file_name = i.group('name') + f'_{count}'
                img_filepath = os.path.join(new_path, file_name + '.jpg')
                with open(img_filepath,'wb') as f:#写入图片文件
                    f.write(resp1.content)
                print(file_name,'的图片下载完成')
            else:
                count=1
                with open(img_filepath,'wb') as f:
                    f.write(resp1.content)
                print(i.group('name'),'的图片下载完成')

print("全部下载完成！")
'''
import re,os

path='中国工程院院士/工程管理学部(77人，其中跨学部院士71人)'
for file in os.listdir(path):
    if file.split('.')[-1]=='txt':
        with open(os.path.join(path,file),encoding='utf-8') as f:
            content=f.read()
            '''key=re.compile(r'(?P<n>.*?)[专,学]家，')
            a=key.findall(content)
            print(a)
            key=re.compile(r'从事(?P<n>.*?)。')
            b=key.findall(content)
            print(b)           
            key=re.compile(r'。(?P<date>.*?)出{0,1}生于(?P<address>.*?)。')
            c=key.findall(content)
            if c==[]:
                key=re.compile(r'。(?P<date>.*?)出{0,1}生，(?P<address>.*?)。')
                c=key.findall(content)
                print(c)
            else:
                print(c)
            '''

'''if c==[]:
    print(os.path.join(path,file))'''