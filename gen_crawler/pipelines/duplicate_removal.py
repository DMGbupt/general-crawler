# -*- coding: utf-8 -*-

"""去重模块
"""

import re
from scrapy.exceptions import DropItem

from gen_crawler.items import *
from gen_crawler.database.auto360_dao import Auto360Dao
from gen_crawler.database.caam_dao import CaamDao
from gen_crawler.database.autohome_dao import AutohomeDao
from gen_crawler.database.chinaev_dao import ChinaevDao
from gen_crawler.database.cpca1_dao import Cpca1Dao

from gen_crawler.logs.crawler_logger import spider_logger


class DuplicateRemoval(object):

    """去重
    """

    def process_item(self, item, spider):
        """去重流程控制
        """

        # 去重
        if isinstance(item, Auto360):
            db = Auto360Dao()
            if self.is_duplicate(item, db):
                db.close()
                return DropItem("Duplicate news found: %s" % item['crawl_url'])
            else:
                db.close()
                return item
        if isinstance(item, Caam):
            db = CaamDao()
            if self.is_duplicate(item, db):
                db.close()
                return DropItem("Duplicate news found: %s" % item['crawl_url'])
            else:
                db.close()
                return item
        if isinstance(item, Autohome):
            db = AutohomeDao()
            if self.is_duplicate(item, db):
                db.close()
                return DropItem("Duplicate news found: %s" % item['crawl_url'])
            else:
                db.close()
                return item
        if isinstance(item, Chinaev):
            db = ChinaevDao()
            if self.is_duplicate(item, db):
                db.close()
                return DropItem("Duplicate news found: %s" % item['crawl_url'])
            else:
                db.close()
                return item
        if isinstance(item, Cpca1):
            db = Cpca1Dao()
            if self.is_duplicate(item, db):
                db.close()
                return DropItem("Duplicate news found: %s" % item['crawl_url'])
            else:
                db.close()
                return item

    def is_duplicate(self, news, db):
        """去重
        :param news: 待判断的新闻
        :return: True/False，是否已被保存在数据库中
        """
        # 数据库中已包含有相同标题的数据,相同URL时标题也一定相同
        if len(db.load_id("crawl_url", news['crawl_url'])) > 0:
            spider_logger.warning("There is a record with the same url of news {0} in the database!"
                                  .format(news['crawl_url']))
            return True
        return False
