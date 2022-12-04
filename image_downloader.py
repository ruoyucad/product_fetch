
import os
import requests
path=os.getcwd()  #设置图片文件路径，前提是必须要有abc这个文件夹
import pandas as pd
df=pd.read_excel('best_root.xlsx', sheet_name='Sheet3')
images_path = path+'\\Ruoyu\images\\'

urls=df['image-src']
for i in range(len(urls)):
    print(i)
    r = requests.request('get',urls[i])  #获取网页
    print(r.status_code)
    
    with open(images_path+str('images')+str(i)+'.jpg','wb') as f:  #打开写入到path路径里-二进制文件，返回的句柄名为f
        f.write(r.content)  #往f里写入r对象的二进制文件
    f.close()