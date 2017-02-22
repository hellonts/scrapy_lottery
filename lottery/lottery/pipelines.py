#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: ylf
#
# Created: 16-12-19

import MySQLdb.cursors
import datetime
import requests
import time
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
from scrapy import log
from items import *

settings = get_project_settings()


class MySQLStorePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == LotteryItem:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            issue = item["issue"]
            table = item["tablename"]
            try:
                select_sql = "SELECT 1 FROM {} WHERE issue = %s".format(table)
                select_param = [issue]
                self.cursor.execute(select_sql, select_param)
                ret = self.cursor.fetchone()
                if ret:
                    pass
                else:
                    if item["opentime"] == "":
                        opentime = now
                    else:
                        opentime = item["opentime"]
                    insert_sql = "insert into {}(issue, opencode, opentime, created_at, updated_at)values" \
                                 "(%s, %s, %s, %s, %s)".format(table)
                    insert_param = [item["issue"], str(item["opencode"]), opentime, now, now]
                    self.cursor.execute(insert_sql, insert_param)
                    self.connect.commit()
            except Exception as error:
                log(error)
            return item
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            issue = item["issue"]
            table = item["tablename"]
            try:
                select_sql = "SELECT 1 FROM {} WHERE issue = %s".format(table)
                select_param = [issue]
                self.cursor.execute(select_sql, select_param)
                ret = self.cursor.fetchone()
                if ret:
                    pass
                else:
                    if item["opentime"] == "":
                        opentime = now
                    else:
                        opentime = item["opentime"]
                    insert_sql = "insert into {}(issue, opencode, opentime, created_at, updated_at)values" \
                                 "(%s, %s, %s, %s, %s)".format(table)
                    insert_param = [item["issue"], str(item["opencode"]), opentime, now, now]
                    self.cursor.execute(insert_sql, insert_param)
                    self.connect.commit()
            except Exception as error:
                log(error)
            return item


