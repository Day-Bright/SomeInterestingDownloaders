# -*- coding: UTF-8 -*-

'''
@Product ：VScode
@File    ：bilibili.py
@Date    ：2022/04/04 22:35:26
@Author  ：XYJ
@Contact ：1520207872@qq.com
'''


import ffmpeg
import time
import os
import sys
import re
import json
import requests
from pprint import pprint
import subprocess


def bilibili_download(url):
    headers = {
        'referer': 'https://www.bilibili.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers).text
    date = re.findall(r'__playinfo__=(.*?)</script>', response)[0]
    inf = re.findall(r'__INITIAL_STATE__=(.*?)\;\(function', response)[0]
    date_json = json.loads(date)
    inf_json = json.loads(inf)
    # pprint(inf_json['videoData'])
    bvid = inf_json['videoData']['bvid']
    title = inf_json['videoData']['title']
    if '/' in title:
        title = title.replace("/"," ")
    video_url = date_json['data']['dash']['video'][0]['baseUrl']
    audio_url = date_json['data']['dash']['audio'][0]['baseUrl']
    video_response = requests.request(
        "GET", video_url, headers=headers).content
    audio_response = requests.request(
        "GET", audio_url, headers=headers).content
    with open('./{bvid}_video.mp4'.format(bvid=bvid), 'wb') as video_file:
        video_file.write(video_response)
    with open('./{bvid}_audio.m4a'.format(bvid=bvid), 'wb') as audio_file:
        audio_file.write(audio_response)
    p = subprocess.Popen(
        "ffmpeg -i {bvid}_video.mp4 -i {bvid}_audio.m4a -vcodec copy -acodec copy {bvid}.mp4".format(bvid=bvid))
    if p.wait() == 0:
        os.unlink('./{bvid}_video.mp4'.format(bvid=bvid))
        os.unlink('./{bvid}_audio.m4a'.format(bvid=bvid))
        os.rename('./{bvid}.mp4'.format(bvid=bvid), './{title}.mp4'.format(title=title))


if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV1zv411K77P?spm_id_from=333.999.0.0"
    bilibili_download(url)
