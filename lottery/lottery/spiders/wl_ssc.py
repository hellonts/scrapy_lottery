#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: ylf
#
# Created: 16-12-19

import scrapy
import re
import time
import os
from scrapy.selector import Selector
from lottery.items import LotteryItem
from scrapy import log
from pubfun import *
from lottery.settings import *


class Wl_xj_sscSpider(scrapy.Spider):
    #新疆时时彩#
    name = "wl_xj_ssc"
    allowed_domains = ["xjflcp.com","kaijiang.500.com"]
    today = time.strftime("%Y%m%d", time.localtime())
    start_urls = [
        "http://www.xjflcp.com/game/sscIndex",
        "http://kaijiang.500.com/static/info/kaijiang/xml/xjssc/{}.xml".format(today),
    ]

    def parse(self, response):
        url = response.url
        item = LotteryItem()
        result = []
        try:
            if url == "http://www.xjflcp.com/game/sscIndex":
                for sel in response.xpath('//div[@class="con_left"]'):
                    item["issue"] = sel.xpath('p/span/text()').extract()[0]
                    item["opencode"] = ','.join(sel.xpath('div/i/text()').extract())
                    item["tablename"] = "wl_xj_ssc"
                    item["opentime"] = ""
                    return item
            elif url == "http://kaijiang.500.com/static/info/kaijiang/xml/xjssc/{}.xml".format(self.today):
                for sel in response.xpath('//xml/row'):
                    if sel:
                        result.append(
                            {"issue":       "{}{}".format(''.join(sel.xpath('@expect').extract())[:8],
                                                          ''.join(sel.xpath('@expect').extract())[9:]),
                             "opencode":    sel.xpath('@opencode').extract()[0],
                             "opentime":    sel.xpath('@opentime').extract()[0],
                             "tablename":   "wl_xj_ssc",
                            })
        except Exception as err:
            log.msg("wl_xj_ssc spider is error: {}".format(str(err)), level=log.ERROR)

        return result


class Wl_tj_sscSpider(scrapy.Spider):
    #天津时时彩#
    name = "wl_tj_ssc"
    allowed_domains = ["kaijiang.500.com","tjflcpw.com"]
    today = time.strftime("%Y%m%d", time.localtime())
    start_urls = [
        "http://www.tjflcpw.com/index.aspx",
        "http://kaijiang.500.com/static/info/kaijiang/xml/tjssc/{}.xml".format(today),
        #"http://kaijiang.aicai.com/tianjin/"
    ]

    def parse(self, response):
        url = response.url
        result = []
        item = LotteryItem()
        try:
            if url == "http://www.tjflcpw.com/index.aspx":
                issue = response.xpath('//a[@href="/report/SSC_WinMessage.aspx"]/text()').extract()[0].replace(" ","")
                src = response.xpath('//img[@id="ImgSSCWinCode"]/@src').extract()[0]
                imgurl = "http://www.tjflcpw.com/{}".format(src)
                os.system('wget {} -O {}.png -c'.format(imgurl, self.name))
                filename = "{}.png".format(self.name)
                fpath = 'wl/ssc/wl_tj_ssc'
                opencode = splitimage(filename, ROWNUM, COLNUM, DSTPATH, fpath)
                os.system('rm -rf {}'.format(filename))
                item["issue"] = "20{}".format(issue[0])
                item["opencode"] = ','.join(opencode)
                item["opentime"] = ""
                item["tablename"] = "wl_tj_ssc"

            elif url == "http://kaijiang.500.com/static/info/kaijiang/xml/tjssc/{}.xml".format(self.today):
                for sel in response.xpath('//xml/row'):
                    if sel:
                        result.append(
                            {"issue":       int(''.join(sel.xpath('@expect').extract())),
                             "opencode":    sel.xpath('@opencode').extract()[0],
                             "opentime":    sel.xpath('@opentime').extract()[0],
                             "tablename":   "wl_tj_ssc",
                            })
            
        except Exception as err:
            log.msg("wl_tj_ssc spider is error: {}".format(str(err)), level=log.ERROR)

        return result


class Wl_cq_sscSpider(scrapy.Spider):
    #重庆时时彩#
    name = "wl_cq_ssc"
    allowed_domains = ["cqcp.net","caipiao.163.com"]
    today = time.strftime("%Y-%m-%d", time.localtime())
    start_urls = [
        "http://buy.cqcp.net/ajaxHTTP/gamedraw/GetOpenNumber.aspx",
        "http://caipiao.163.com/award/"
    ]


    def parse(self, response):
        url = response.url
        item = LotteryItem()
        try:
            if url == "http://buy.cqcp.net/ajaxHTTP/gamedraw/GetOpenNumber.aspx":
                 body = {"sPass":"BEAB95B0BAA1242CF042D1659686F54B","idMode":'8',"iType":'2',"iCount":'1'}
                 return [scrapy.http.FormRequest(
                    url="http://buy.cqcp.net/ajaxHTTP/gamedraw/GetOpenNumber.aspx", method='POST',formdata = body,
                     callback=self.parsepost)]
            elif url == "http://caipiao.163.com/award/":
                i = 0
                for sel in response.xpath('//table[@class="awardList"]/tbody/tr'):
                    if i == 27:
                        item["issue"] = int("20{}".format(re.findall(r"\d+\.?\d*",
                                                        sel.xpath('td[@class="period"]/a/text()').extract()[0])[0]))
                        item["opentime"] = "{} {}:00".format(self.today,
                                            ':'.join(re.findall(r"\d+\.?\d*",sel.xpath('td/text()').extract()[0])))
                        item["opencode"] = ','.join(sel.xpath('td/em/text()').extract())
                        item["tablename"] = "wl_cq_ssc"
                    i+=1
        except Exception as err:
            log.msg("wl_cq_ssc spider is error: {}".format(str(err)), level=log.ERROR)


    def parsepost(self, response):
        items = []
        result = []
        for sel in response.xpath('//table/tr'):
            doc = ''.join(sel.xpath('td/text()').extract())
            if len(doc) > 4 and doc != u'期号五星三星二星一星大小单双开奖时间':
                result.append(doc.replace(u'\xa0', u' '))
                if len(result) == 2:
                    opent = result[0].split(',')[3][2:]
                    if len(opent) == 15:
                        opentime = "{} {}".format(opent.split(' ')[0],"0"+ opent.split(' ')[1])
                    else:
                        opentime = opent
                    items.append(
                        {"issue":       int(result[0][:11]),
                         "opencode":    ','.join(result[1]),
                         "opentime":    opentime,
                         "tablename":   "wl_cq_ssc"
                        })

                    result = []
        return items

