# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

class PandafangPipeline(object):
    def __init__(self):
        self.data={}


    def process_item(self, item, spider):
        if self.data.has_key(item['fn']):
            pass
        else:
            self.data[item['fn']]=[]
        line=item['dong']+','+ item['unit']+','+item['layer']+','+item['area']+','+item['price']+','+item['fang']+','+item['name']+','+item['url']+"\n"
        self.data[item['fn']].append(line)
        return item

    def close_spider(self,spider):
        for key in self.data.keys():
            ls=self.data[key]
            f = file(key+'.csv', 'wb')
            f.write(codecs.BOM_UTF8) 
            f.writelines(ls)
            f.close()


