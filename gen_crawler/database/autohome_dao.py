# -*- coding: utf-8 -*-
from dao import Dao
from gen_crawler.logs.crawler_logger import spider_logger


class AutohomeDao(Dao):

    _sql_save_info = """insert into industry_info (title, digest, content, image, author, keyword, publish_time, source_website, source_url, crawl_website, crawl_url) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    _sql_load_info_id = """select id from industry_info where {0} = %s"""
    _sql_save_info_attachment = """insert into industry_info_attachment (name, file, info_id) values(%s, %s, %s)"""


    def save(self, news):
        try:
            cur = self.conn.cursor()
            # 准备参数
            param_info = (news['title'], news['digest'], news['content'], news['image_path'], news['author'], news['keyword'], news['publish_time'], news['source_website'], news['source_url'], news['crawl_website'], news['crawl_url'])
            # 插入资讯表单
            cur.execute(AutohomeDao._sql_save_info, param_info)
            if news['atc'] == 1:
                cur.execute(AutohomeDao._sql_load_info_id.format("crawl_url"),(unicode( news['crawl_url']),) )
                info_id = cur.fetchone()[0]
                param_info_attachment = (news['atc_name'], news['atc_path'], info_id)
                cur.execute(AutohomeDao._sql_save_info_attachment, param_info_attachment)
            self.conn.commit()
        except Exception, e:
            spider_logger.error("[MySQL] Flush autohome news to database failed, because of {0} !".format(e))
            self.conn.rollback()
        finally:
            cur.close()

    _sql_load_id = """select id from industry_info where {0} = %s"""

    def load_id(self, attribute, value, size=None):
        """选择attribute为value的行的id
        :param attribute: 属性
        :param value: 值
        :param size: 返回结果条数
        :return: select结果
        """
        cur = self.conn.cursor()
        cur.execute(self._sql_load_id.format(attribute),(unicode(value),) )
        rel = cur.fetchmany(size)
        cur.close()
        return rel
