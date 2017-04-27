# -*- coding: utf-8 -*-

# Scrapy settings for pandafang project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pandafang'

SPIDER_MODULES = ['pandafang.spiders']
NEWSPIDER_MODULE = 'pandafang.spiders'

ITEM_PIPELINES = {  
    'pandafang.pipelines.PandafangPipeline': 1
}
DOWNLOAD_DELAY=0.3
DOWNLOAD_TIMEOUT=30
COOKIES_ENABLED=False

HEADER = {
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "USER_AGENT" :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    "Connection":"keep-alive",
    "Host":"119.97.201.28:8087",
    "Referer":"http://119.97.201.28:8087/xmqk.asp"
}

