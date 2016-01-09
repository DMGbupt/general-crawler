# -*- coding: utf-8 -*-
"""autochina360网站持久化类
"""
import re
from gen_crawler.items import Auto360
from gen_crawler.database.auto360_dao import Auto360Dao
from gen_crawler.logs.crawler_logger import spider_logger


class Auto360Pipeline(object):

    """持久化类
    """

    def __init__(self):
        self.db = Auto360Dao()

    def process_item(self, item, spider):
        """缓存
        """
        if not isinstance(item, Auto360):
            return item
        # 检查必要属性
        for attr in ('crawl_url', 'title', 'source_website', 'publish_time', 'content'):
            if not item[attr]:
                spider_logger.warning(
                    "[Auto360_pipeline] Item of {0} lack {1}".format(item['crawl_url'], attr))
                return
        # 填充非必要属性
        try:
            if 'digest' not in item:
                item['digest'] = re.sub(
                    "<.{1,3}?>", "", item['content'][0:400])
        except Exception, e:
            spider_logger.warning(
                "Can't get digest from %s" % item['crawl_url'])
        if 'author' not in item:
            item['author'] = "plustock"
        if 'source_url' not in item:
            item['source_url'] = item['crawl_url']
        for attr in ('digest', 'image_path', 'keyword'):
            if attr not in item:
                item[attr] = None

        # 保存
        self.db.save(item)

    def close_spider(self, spider):
        self.db.close()
