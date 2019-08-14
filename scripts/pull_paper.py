# -*- coding:utf-8 -*- 
__Author__ = "Feiyang Chen"
__Time__ = '2019-08-14'
__Title__ = 'Automatic crawling of Multimodal related papers Test'

"""
 code is far away from bugs with the god animal protecting
    I love animals. God bless you.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃ God Bless  ┣┓
                ┃ Bug-Free!  ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import re
import requests
import urllib.request
import os
import argparse

parser = argparse.ArgumentParser(description="pull_paper")
parser.add_argument('--keyword', type=str, default='Multimodal')  # Match the keywords we want to find the paper
args = parser.parse_args()

# get web context
r = requests.get('http://openaccess.thecvf.com/CVPR2018.py')

data = r.text
# find all pdf links
link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)", data)
name_list = re.findall(r"(?<=href=\").+?2018_paper.html\">.+?</a>", data)

cnt = 1
num = len(link_list)
# your local path to download pdf files
localDir = './CVPR2018/{}/'.format(args.keyword)
if not os.path.exists(localDir):
    os.makedirs(localDir)
while cnt < num:
    url = link_list[cnt]
    # seperate file name from url links
    file_name = name_list[cnt].split('<')[0].split('>')[1]
    # to avoid some illegal punctuation in file name
    file_name = file_name.replace(':', '_')
    file_name = file_name.replace('\"', '_')
    file_name = file_name.replace('?', '_')
    file_name = file_name.replace('/', '_')
    file_name = file_name.replace(' ', '_')
    search_list = file_name.split('_')
    search_pattern = re.compile(r'{}'.format(args.keyword), re.IGNORECASE)

    download_next_paper = True

    # print([True for i in search_list if search_pattern.findall(i)])
    if ([True for i in search_list if search_pattern.findall(i)]):
        download_next_paper = False

    if download_next_paper:
        cnt = cnt + 1
        continue

    file_path = localDir + file_name + '.pdf'
    if os.path.exists(file_path):
        print('File 【{}.pdf】 exists,skip downloading.'.format(file_name))
        cnt = cnt + 1
        continue
    else:
        # download pdf files
        print('[' + str(cnt) + '/' + str(num) + "]  Downloading -> " + file_path)
        try:
            urllib.request.urlretrieve('http://openaccess.thecvf.com/' + url, file_path)
        except:
            cnt = cnt + 1
            continue
        cnt = cnt + 1
print("all download finished")
