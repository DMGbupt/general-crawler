# -*- coding: utf-8 -*-

"""
已设置失败重连次数为3次。
"""

import re
from datetime import datetime
import urllib
import json

from scrapy import Request

from gen_crawler.items import Autohome
from gen_crawler.index_spider import IndexSpider
from gen_crawler.utils.html_formatter import HtmlFormatter
from gen_crawler.configs.autohome_config import CONF
from gen_crawler.logs.crawler_logger import spider_logger


class CaamNews(IndexSpider):

    name = "autohome"
    _config = CONF

    def _get_result(self, response, config):
        rel = []
        conf = config
        decoded_json = json.loads(response.body.decode('gb2312'))
        new_data = decoded_json[0]['Article']
        if not new_data:
            spider_logger.error(
                "Can't get url json data from %s" % conf['url'])
            return
        # 提取搜索结果
        for result in new_data:
            item = Autohome()
            Dir = result['Dir']
            PublishTime = result['PublishTime']
            Id = result['Id']
            item['crawl_url'] = "http://www.autohome.com.cn" + \
                Dir+PublishTime+"/"+str(Id)+".html"
            item['title'] = result['Title']
            item['digest'] = result['Summary']
            item['icon'] = result['Img']
            item['keyword'] = conf['keyword']
            item['publish_time'] = None
            rel.append(item)
        return rel

    def _next_result_page(self, response):
        decoded_json = json.loads(response.body.decode('gb2312'))
        next_data = decoded_json[0]
        page = int(next_data['CurrentPage'])
        maxpage = int(next_data['Total'])
        crawlpage = 3
        if page < (maxpage if self.crawl_mode == 1 else(crawlpage if crawlpage<maxpage else maxpage)):
            page += 1
        else:
            spider_logger.info("Get last index page: %s" % response.url)
            return
        next_url = re.split("&page=|&ExcptArtIds=", response.url)
        return next_url[0]+"&page="+str(page)+"&ExcptArtIds="+next_url[2]

    def _finish_item(self, item, response):
        # 继续提取信息
        '''
        if response.xpath("//div[@class='page']").extract():
            item['crawl_url'] = item['crawl_url'].replace(".html", "-all.html")
            yield Request(item['crawl_url'], callback=self.parse_page, meta={'conf': conf, 'item': item})
        '''
        item['crawl_website'] = u"汽车之家"
        item['atc'] = 0
        publish_time = response.xpath("//div[@class='article-info']/span[1]/text()").extract()[0]
        item['publish_time'] = datetime.strptime(publish_time.replace(
            u'年', "-").replace(u'月', "-").replace(u'日', "").strip()+":00", "%Y-%m-%d %H:%M:%S")
        item['source_website'] = u"来源："+response.xpath(
            "//div[@class='article-info']/span[2]/a/text()").extract()[0]
        # content
        content = response.xpath("//div[@class='article-content']").extract()
        item['content'] = HtmlFormatter.format_content(content[0])
        # image
        item['image_urls'] = []
        for img_url in response.xpath("//div[@class='article-content']//img/@src").extract():
            if re.match("http.*", img_url):
                item['image_urls'].append(img_url)
        return item
