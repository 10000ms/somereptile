#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
百度贴吧爬虫
参考：https://github.com/Ehco1996/Python-crawler/blob/master/Beautiful%20Soup%20%E7%88%AC%E8%99%AB/baidutieba.py
'''

# 导入必要的库
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re


# 设置要爬取的贴吧名
tieba_name = '崩坏3'
# 设置要爬取的页面数量
deep = 3


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "


def get_content(url):
    '''
    分析贴吧的网页文件，整理信息，保存在列表变量中
    '''

    # 初始化一个列表来保存所有的帖子信息：
    comments = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_html(url)

    # 我们来做一锅汤
    soup = BeautifulSoup(html, 'lxml')

    # 按照之前的分析，我们找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    # 通过循环找到每个帖子里的我们需要的信息：
    for li in liTags:
        # 初始化一个字典来存储文章信息
        comment = {}
        # 这里使用一个try except 防止爬虫找不到信息从而停止运行
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            # comment['link'] = "http://tieba.baidu.com/" + \
            #     li.find('a', attrs={'class': 'j_th_tit '})['href']
            # comment['name'] = li.find(
            #     'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except BaseException as e:
            print('出了点小问题:'+e.__str__())

    return comments


def Out2File(dict):
    '''
    将爬取到的文件写入到本地
    保存到当前目录的 result.txt文件中。

    '''
    with open('result.txt', 'a+', encoding='utf8') as f:
        for comment in dict:
            # f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
            #     comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
            f.write('标题：{} \n 发帖时间：{} \n 回复数量： {} \n\n'
                    .format(comment['title'], comment['time'], comment['replyNum']))

        print('当前页面爬取完成')


def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    #循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有的信息都已经保存完毕！')


def check_url(tieba_name):
    url_name = urllib.parse.quote( tieba_name)
    test_url = 'http://tieba.baidu.com/f?kw=' + url_name + '=utf-8'
    content = BeautifulSoup(get_html(test_url), 'lxml')
    is_target = re.search('name="description"',str(content))
    if is_target:
        print('找到'+ tieba_name +'贴吧')
    else:
        print('未找到' + tieba_name + '贴吧')
    main(test_url, deep)


if __name__ == '__main__':
    check_url(tieba_name)


