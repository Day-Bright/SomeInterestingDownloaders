#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   FictionDownload.py
@Time    :   2023/12/31 11:43:48
@Author  :   DoweaNn 
@Contact :   1520207872@qq.com
@product :   VScode
'''

#书源：爱下书小说网http://www.aixiashu.info/

# here put the import lib

import requests
import re
from bs4 import BeautifulSoup



def get_fiction_id(my_author,my_fiction):
    search_url = "http://www.aixiashu.info/modules/article/search.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': 'http://www.aixiashu.info',
        'referer': 'http://www.aixiashu.info/modules/article/search.php',
        'Host': 'www.aixiashu.info'
    }
    date = {
        'searchkey': my_fiction,
        'searchtype': 'articlename'
    }
    response = requests.post(url=search_url,headers=headers,data=date)
    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
    soup_table = soup.find('table')
    soup_trs = soup_table.find_all('tr')
    for tr in soup_trs:
        tds = tr.find_all('td')
        if len(tds)==0:
            pass
        else:
            fiction_name=tds[0].text
            fiction_author=tds[2].text
            if my_author==fiction_author and my_fiction==fiction_name:
                return tds[0].a['href'].split('/')[-2]
            else:
                pass
                # fiction_dict["fiction_name"]=tds[0].text
                # fiction_dict["fiction_author"]=tds[2].text
                # fiction_dict["fiction_href"]=tds[0].a['href']
                # fiction_dict["fiction_id"]=tds[0].a['href'].split('/')[-2]
                # print(fiction_dict)
                
                
def download(id):
    fiction_download_url = 'http://txt.aixiashu.info/modules/article/txtarticle.php?id='+id
    headers = {
        'referer': 'http://www.aixiashu.info/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    fiction_download_response = requests.get(url=fiction_download_url,headers=headers)
    with open(r"{id}.txt".format(id=id), "wb") as fiction_txt:
        fiction_txt.write(fiction_download_response.content)
        

def read_large_file(file_name):
    with open(file_name,'r', encoding='utf-8') as file:
        for line in file:
            yield line


def analyze(file_name):
    all_line = ""
    k=0
    file_generator = read_large_file(r"{id}.txt".format(id=file_name)) 
    number_of_chapters=1
    for line in file_generator:
        k+=1
        if k==2:
            pattern = r'[^\w\s]' 
            line = re.sub(pattern, '', line) 
            title=line
            number_of_chapters+=1
        all_line+=line
        if "------------\n" == line:
            k=0
            all_line+=line
            file = open(r"{number_of_chapters}{title}_.txt".format(number_of_chapters=number_of_chapters,title=title[:-1]), 'w',encoding="utf-8")
            file.write(all_line)
            file.close()
            all_line=""
    

if __name__ == '__main__':
    my_fiction = "遮天"
    my_author = '辰东'
    id = get_fiction_id(my_author,my_fiction)
    download(id=id)
    analyze(file_name=id)