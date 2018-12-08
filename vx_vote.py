# -*- coding:utf-8 -*-
# @Time      :2018/12/6 21:01
# @Author    :wanhaoran
# @FileName  :vx_vote.py

import random
import re
import string
import time

from bs4 import BeautifulSoup
import requests


class Ip_List:
    """
    ip代理池
    """

    def __init__(self):
        self.ip_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        self.proxy = {
            "http":"60.191.201.38:45461"
        }

    def get_ip_list(self):
        """
        从网站爬取ip_list
        :return:
        """
        for page in range(1, 20):
            url = "http://www.xicidaili.com/nn/" + str(page)
            web_data = requests.get(url=url, headers=self.headers,proxies = self.proxy)
            print(web_data)
            soup = BeautifulSoup(web_data.text, "lxml")
            ips = soup.find_all('tr')
            print(ips)
            for i in range(2, len(ips)):
                ip_info = ips[i]
                print(ip_info)
                tds = ip_info.find_all('td')
                self.ip_list.append(( tds[5].text,tds[1].text + ":" + tds[2].text))

        return self.ip_list


    def get_random_ip(self):
        """
        :return: 1.http还是https 2.ip
        """
        random_one = random.choice(self.ip_list)
        return random_one[0].lower(), random_one[1]


class Vote:
    def __init__(self):
        self.activityId = 
        self.playerId = 
        self.number = 
        self.activityName = 
        self.isGift = 
        self.success_url = 
        self.vote_url = 

    @staticmethod
    def random_sleep_time(digits_length):
        """
        随机睡眠
        :param digits_length:
        :return:
        """
        digits_char = string.digits
        need_sleep_time = ''
        for i in range(digits_length):
            need_sleep_time += random.choice(digits_char)
        return int(need_sleep_time) + 2

    def get_open_id(self):
        def getRandomString(id_length):
            charSeq = string.ascii_letters + string.digits
            randString = ''
            for i in range(id_length):
                randString += random.choice(charSeq)
            return randString

        return getRandomString(16) + "-" + getRandomString(11)

    def success(self, open_id, ip_t):
        """
        访问第一个页面，得到参数
        :param open_id: open_id
        :param ip_t: ip状态和ip地址
        :return: 返回得到的两个钩子参数
        """
        url = self.success_url

        proxy = {
            ip_t[0]: ip_t[1]
        }

        params = {
            "activityId": self.activityId,
            "openId": open_id,
            "playerId": self.playerId,
            "number": self.number,
            "activityName": self.activityName,
            "isGift": self.isGift
        }

        headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            # "Connection": "keep-alive",
            # "Cookie": "JSESSIONID=BEDA66485B52B1FB4C916C39499EA081",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; U;  zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger"
        }

        # params = parse.urlencode(params)
        # print(params)
        r = requests.get(url=url, params=params, headers=headers, proxies=proxy)
        html = r.text
        # soup = BeautifulSoup(html,"html.parser")

        # 正则找出埋的钩子参数
        pattern1 = re.compile(r'var _0sdfad="(.*?)"', re.MULTILINE | re.DOTALL)
        pattern2 = re.compile(r'var _0ees88="(.*?)"', re.MULTILINE | re.DOTALL)
        index1 = re.search(pattern1, html)
        index2 = re.search(pattern2, html)
        res1 = index1.group().replace(r'var _0sdfad="', "").replace('"', '')
        res2 = index2.group().replace(r'var _0ees88="', "").replace('"', '')
        # print(soup)
        return res1, res2

    def vote_real(self, open_id, ip_t):
        index1, index2 = self.success(open_id, ip_t)
        url = self.vote_url +"/"+ index2 + "/" + index1

        proxy = {
            ip_t[0]: ip_t[1]
        }

        params = {
            "activityId": self.activityId,
            "openId": open_id,
            "playerId": self.playerId
        }

        headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            # "Connection": "keep-alive",
            # "Cookie": "JSESSIONID=BEDA66485B52B1FB4C916C39499EA081",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; U;  zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger"
        }
        r = requests.post(url=url, params=params, headers=headers, proxies=proxy)
        print(r)

    def do(self, ip_t):
        open_id = self.get_open_id()
        self.vote_real(open_id, ip_t)


class FileWriter(object):
    def writer(self, text):
        with open('ip_list.txt', 'a', encoding='utf-8') as f:
            f.write(text + '\n')


if __name__ == "__main__":

    ipList = Ip_List()
    ipList.get_ip_list()
    vote = Vote()
    file_writer = FileWriter()
    success_count, error_count = 0, 0
    ip_useful_list = []
    for i in range(5):
        try:
            ip_t = ipList.get_random_ip()
            print(ip_t)
            vote.do(ip_t=ip_t)
            random_wait_time = vote.random_sleep_time(1)
            time.sleep(random_wait_time)
        except Exception:
            error_count += 1
            print("error_count: ",error_count)
        else:
            print("success_count: ",success_count)
            success_count += 1
            if ip_useful_list.count(ip_t)==0:
                ip_useful_list.append(ip_t)
        print("---")

    for ip_t in ip_useful_list:
        file_writer.writer(ip_t[0]+" "+ip_t[1])
