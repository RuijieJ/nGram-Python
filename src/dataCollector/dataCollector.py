#!/usr/bin/python
import os, time, sys
import re
import urlparse
import requests
from bs4 import BeautifulSoup

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"

class Spider():
    def __init__(self, year, month, day):
        self.host = "http://news.sina.com.cn/"
        self.url = "http://news.sina.com.cn/old1000/news1000_" + str(year) + str(month).zfill(2) + str(day).zfill(2) + ".shtml"
        self.year = year
        self.month = month
        self.day = day
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': agent})
        self.s.headers.update({'Referer': self.host })

    def parse_list(self):
        print "getting url: " + self.url,
        sys.stdout.flush()
        try:
            r = self.s.get(self.url, timeout=5)
        except:
            time.sleep(10)
            return
        print " done"
        sys.stdout.flush()
#        print r.content
        soup = BeautifulSoup(r.content.decode('gbk','ignore'), 'lxml' )
        tags = soup.select("ul li a")
        print "tags got"
        for _tag in tags:
            tag = str(_tag)
            start = len("<a href=\"")
            end = start + 1
            while tag[end] != '"':
                end += 1
            url = tag[start:end]
            if not url.startswith("http"):
                url = "http://news.sina.com.cn" + url
            if url.find("cgi-bin") != -1:
                continue
            print "Crawl:",  url
            num_try = 0
            get_content = 0
            while get_content == 0:
                try:
                    print "\tgetting page: " + url + ", num-try = " + str(num_try) + "..."
                    sys.stdout.flush()
                    page_r = self.s.get(url, timeout=3)
                    get_content = 1
                    print "\tdone"
                    sys.stdout.flush()
                except:
                    time.sleep(2 + num_try)
                    num_try += 1
                    if num_try > 5:
                        break
            if num_try > 10:
                continue
            page_soup = BeautifulSoup(page_r.content.decode('gbk', 'ignore'), 'lxml')
            find_res = page_soup.find_all("font", id="zoom")
            if len(find_res) == 0:
                print "No Content"
                continue
#            print page_r.content
            content = ""
            for tag in page_soup.select("#zoom > p"):
                print tag
                content += str(tag)
            f = open("results/" + str(self.year) + str(self.month).zfill(2) + str(self.day).zfill(2) + ".txt", "a")
            f.write(content)
            f.close()
            print r.content[:20]

def main():
    print "Welcome!"
    year = 2006
    month = 4
    os.system("mkdir results")
    for day in range(6, 10):
        if month == 2 and day > 28:
            break
        spider = Spider(year, month, day)
        spider.parse_list()
    pass

if __name__ == "__main__":
    main()
