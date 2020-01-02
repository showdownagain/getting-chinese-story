#coding:utf-8
import  requests
from bs4 import BeautifulSoup
import re
import os
import time
import sys
import ssl

#https的 ssl证书处理
ssl._create_default_https_context = ssl._create_unverified_context 
#请求头
req_header={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate，br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cookie':'UM_distinctid=16ec3fa5cea7f-08ddf32fa381a3-2393f61-100200-16ec3fa5ceb22b; __cfduid=de16afbd245144d753d92b8f64d555ce71575435497; CNZZDATA1261736110=288883036-1575245968-%7C1576804966; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1575593545,1575593556,1576633960,1576809438; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1576809574',
'Host':'www.jx.la',
'Proxy-Connection':'keep-alive',
'referer':'https://www.jx.la/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
#小说主地址
req_url_base='https://www.jx.la/book/'           
#下载函数
#root_url 章节根地址
#page_number 章节地址编号
#count_time 超时判定时间
def manage_timeout(root_url,page_number,count_time):
    condition = False
    while not condition:
        try:
            result = requests.get(root_url+str(page_number),params=req_header,timeout=count_time)
            return result
        except requests.exceptions.RequestException:
            time.sleep(1)
            condition = False
            print('尝试重新下载！！')
#小说处理函数
#txt_id：小说编号
#txt字典项介绍
#id：小说编号
# title：小说题目
# first_page：第一章页面
# txt_section：章节地址
# section_name：章节名称
# section_text：章节正文
# section_ct：章节页数
def get_txt(txt_id):
    txt={}
    txt['title']=''
    txt['id']=str(txt_id)
    req_url=req_url_base+ txt['id']+'/'                        #根据小说编号获取小说URL
    print("小说编号："+txt['id'])
    res=requests.get(req_url,params=req_header)             #获取小说目录界面
    soups=BeautifulSoup(res.text,"html.parser")           #soup转化
    #获取小说题目
    txt['title']=soups.select('#wrapper .box_con #maininfo #info h1')[0].text
    txt['author']=soups.select('#wrapper .box_con #maininfo #info p')
    #获取小说最近更新时间
    txt['update']=txt['author'][2].text
    #获取最近更新章节名称
    txt['lately'] = txt['author'][3].text
    #获取小说作者
    txt['author']=txt['author'][0].text
    #获取小说简介
    txt['intro']=soups.select('#wrapper .box_con #maininfo #intro')[0].text.strip()
    print("编号："+'{0:0>8}   '.format(txt['id'])+  "小说名：《"+txt['title']+"》  开始下载。")
    print("正在获取所有章节地址。。。")
    #获取小说所有章节信息
    all_page_address1=soups.select('#wrapper .box_con #list dl dd a')
    #获取小说总章页面数
    all_page_address = all_page_address1[12::]
    section_ct=len(all_page_address)
    print("小说章节页数："+str(section_ct))
    #打开小说文件写入小说相关信息
    fo = open('{0:0>8}-{1}.txt.download'.format(txt['id'],txt['title']), "ab+")
    fo.write((txt['title']+"\r\n").encode('UTF-8'))
    fo.write((txt['author'] + "\r\n").encode('UTF-8'))
    fo.write((txt['update'] + "\r\n").encode('UTF-8'))
    fo.write((txt['lately'] + "\r\n").encode('UTF-8'))
    fo.write(("*******简介*******\r\n").encode('UTF-8'))
    fo.write(("\t"+txt['intro'] + "\r\n").encode('UTF-8'))
    fo.write(("******************\r\n").encode('UTF-8'))
    #获取每一章节信息
    for one_page_info in all_page_address:
        r = manage_timeout(req_url,one_page_info['href'],count_time=5)#请求当前章节页面
        #soup转换
        soup=BeautifulSoup(r.text,"html.parser")
        #获取章节名称
        section_name=soup.select('#wrapper .content_read .box_con .bookname h1')[0]
        section_text=soup.select('#wrapper .content_read .box_con #content')[0]
        for ss in section_text.select("script"):   #删除无用项
            ss.decompose()
        #获取章节文本
        section_text=re.sub( '\s+', '\r\n\t', section_text.text).strip('\r\n')#
        #以二进制写入章节题目
        fo.write(('\r'+section_name.text+'\r\n').encode('UTF-8'))
        #以二进制写入章节内容
        fo.write((section_text).encode('UTF-8'))
        print(txt['title']+' 章节：'+section_name.text+'     已下载')
    fo.close()
    os.rename('{0:0>8}-{1}.txt.download'.format(txt['id'],txt['title']), '{0:0>8}-{1}.txt'.format(txt['id'],txt['title']))
