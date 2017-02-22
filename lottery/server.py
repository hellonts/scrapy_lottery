#!/usr/bin/python 
# -*- coding: utf-8 -*- 

# 
# Author: ylf 
# 
# Created: 16-12-19 

import time 
import sys 
import logging 
import commands 
import os 
from apscheduler.schedulers.background import BlockingScheduler

ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S' 
logging.basicConfig() 



def wl_xj_ssc(): 
    """ 
    新疆时时彩 
    """ 
    logging.info("{}: [{}] start running...".format(time.strftime(ISOTIMEFORMAT, time.localtime(time.time())), 
                                                sys._getframe().f_code.co_name)) 
    try: 
        out = os.system('scrapy crawl wl_xj_ssc') 
        logging.warning("wl_xj_ssc:{}".format(out)) 
        # (status, output) = commands.getstatusoutput('scrapy crawl wl_xj_ssc') 
        # logging.info((status, output)) 
    except Exception as e: 
        logging.error(e) 


def wl_tj_ssc(): 
    """ 
    天津时时彩 
    """ 
    logging.info("{}: [{}] start running...".format(time.strftime(ISOTIMEFORMAT, time.localtime(time.time())), 
                                                sys._getframe().f_code.co_name)) 
    try: 
        out = os.system('scrapy crawl wl_tj_ssc') 
        logging.warning("wl_tj_ssc:{}".format(out)) 
        # (status, output) = commands.getstatusoutput('scrapy crawl wl_tj_ssc') 
        # logging.info((status, output)) 
    except Exception as e: 
        logging.error(e) 


def wl_cq_ssc(): 
    """ 
    重庆时时彩 
    """ 
    logging.info("{}: [{}] start running...".format(time.strftime(ISOTIMEFORMAT, time.localtime(time.time())), 
                                                sys._getframe().f_code.co_name)) 
    try: 
        out = os.system('scrapy crawl wl_cq_ssc') 
        logging.warning("wl_cq_ssc:{}".format(out)) 
        # (status, output) = commands.getstatusoutput('scrapy crawl wl_cq_ssc') 
        # logging.info((status, output)) 
    except Exception as e: 
        logging.error(e) 


def server_start(): 
    """ 
    程序启动入口 
    :return: 
    """ 
    try: 
        scheduler = BlockingScheduler() 
        scheduler.add_job(wl_xj_ssc, trigger='cron', day='*', hour='00-02,10-23', minute='*', second='*/5', id="1") 
        scheduler.add_job(wl_cq_ssc, trigger='cron', day='*', hour='0-02,10-23', minute='*', second='*/5', id="2") 
        scheduler.add_job(wl_tj_ssc, trigger='cron', day='*', hour='09-23', minute='*', second='*/5', id="3") 
        scheduler.start() 
    except Exception as e: 
        logging.error(e) 


if __name__ == '__main__': 
    server_start() 
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C')) 
    try: 
        server_start() 
    except (KeyboardInterrupt, SystemExit): 
        scheduler = BlockingScheduler() 
        scheduler.shutdown() 
