# -*- coding: UTF-8 -*-
from scrapy.spider import Spider
from scrapy.http import FormRequest
from scrapy.selector import Selector
from pandafang.settings import *
from pandafang.items import PandafangItem
import urllib
import requests
from lxml import etree

class FangSpider(Spider):
    name = "pandafang"
    allowed_domains = ["119.97.201.28"]

    def select_pro(self):
        blname=raw_input("input project name:")
        pros=self.req_ls(blname)
        num=int(raw_input("input num:"))
        if num==None or num==0 or num>len(pros):
            print "input error !"
        else:
            return pros[num-1][1]

    def req_ls(self,blname,page=1):#预留一个翻页，现在懒得做
        blname=urllib.quote(blname)
        url=self.root_url+"xmqk.asp?page="+str(page)+"&domain=&blname="+blname+"&bladdr=&prname="
        print url
        rs=requests.get(url)
        rs.encoding='gbk'
        return self.parse_ls(rs.text)


    def parse_ls(self, response):
        dom = etree.HTML(response)
        pros=[]
        i=0
        for l in dom.xpath('//tr[contains(@align,"middle")]/td/a[contains(@href,"3.asp?")]'):
            i+=1
            name=l.getchildren()[0].text
            key=urllib.quote(unicode(l.get('href').split("=")[1]).encode("gbk"))
            print i,name
            pros.append((name,key))
        return pros


    def __init__(self): 
        self.headers = HEADER
        self.root_url = "http://119.97.201.28:8087/"
        prokey=self.select_pro()
        if prokey != None:
            self.start_url = self.root_url + "4.asp?DengJh="+prokey

    def start_requests(self):
        yield FormRequest(self.start_url,
            headers = self.headers,
            encoding='utf-8',
            callback=self.parse_list)

    def parse_list(self, response):
        selector = Selector(response)
        for detail in selector.xpath('//tr[contains(@align,"middle")]/td/a[contains(@href,"5.asp?")]'):
            name=detail.xpath('span/text()').extract()[0].strip()
            url=self.root_url+detail.xpath('@href').extract()[0].encode('gbk')
            yield FormRequest(url,
                    headers = self.headers,
                    encoding='gbk',
                    callback=lambda response,cvsname=name: self.parse_detail(response,cvsname))

    def parse_detail(self, response,cvsname):
        ls=[]
        selector = Selector(response)
        for tr in selector.xpath('//a[contains(@href,"6.asp?gid=")]/ancestor::tr[1]'):
            l=[]
            l.append(tr.xpath('td/text()').extract()[0].strip().encode('utf-8'))
            l.append(tr.xpath('td/text()').extract()[1].strip().encode('utf-8'))
            l.append(tr.xpath('td/text()').extract()[2].strip().encode('utf-8'))
            l.append(cvsname)
            for a in tr.xpath('td//a'):
                url=self.root_url+a.xpath('@href').extract()[0]
                name=a.xpath('text()').extract()[0].strip()
                al=[]
                al.append(name.encode('utf-8'))
                al.append(url.encode('utf-8'))
                if "0000-0000" in url :
                    self.no_price(l,al)
                else:
                    yield FormRequest(url,
                    headers = self.headers,
                    encoding='gbk',
                    callback=lambda response,line=l,al=al:self.parse_price(response,line,al))

    def no_price(self,l,al):
        item = PandafangItem()
        item['dong']=l[0]
        item['unit']=l[1]
        item['layer']=l[2]
        item['fn']=l[3]
        item['fang']=al[0]
        item['url']=al[1]
        item['name']=''
        item['area']=''
        item['price']=''
        yield item

    def parse_price(self,response,l,al):
        s = Selector(response)
        trs = s.xpath('//table/tr[5]/..')
        for tr in trs:
            item = PandafangItem()
            item['dong']=l[0]
            item['unit']=l[1]
            item['layer']=l[2]
            item['fn']=l[3]
            item['fang']=al[0]
            item['url']=al[1]
            item['name']=tr.xpath('tr[1]/td[2]/text()').extract()[0].strip().encode('utf-8')
            item['area']=tr.xpath('tr[3]/td[2]/text()').extract()[0].strip().encode('utf-8')
            item['price']=tr.xpath('tr[5]/td[2]/text()').extract()[0].strip().encode('utf-8')
            yield item

