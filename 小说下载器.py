#coding:utf-8
#!/usr/bin/env python
from urllib.request import urlopen#用于获取网页
from bs4 import BeautifulSoup#用于解析网页
import re
import urllib
import os
from newlearning import get_txt
from deliverbook import sent_eml

def selectfile(txt_name):  
    file_list = os.listdir()
    for i in file_list:
        if txt_name in i:
            return i 

def to_url(ori_string):
    url_code = urllib.parse.quote(ori_string)
    return url_code
while 1>0: 
    name_first = input('请输入正确书名:')
    bookname = name_first
    b = to_url(name_first)
    temp_url = 'https://sou.xanbhx.com/search?siteid=qula&q='+b
    html = urlopen(temp_url)
    bsObj = BeautifulSoup(html, 'html.parser')
    t1 = bsObj.find_all('a')
    links=[]
    dic_1={}
    for t2 in t1:
        t3 = t2.string
        check_name1 = re.findall("[\u4e00-\u9fa5]+",t3)
        check_name = ''.join(check_name1)
        dic_1[check_name] = t2.get('href')
    if bookname in dic_1.keys():
        axe = dic_1[bookname]
        bookid = re.findall(r'\d+\.?\d*',axe)
        temp_id = ''.join(bookid)
        final_id = int(temp_id)
        get_txt(final_id)
        temp_name = selectfile(bookname)
        sent_eml(temp_name)
    else:
        print('搜不到这本书')
        continue
    
    


