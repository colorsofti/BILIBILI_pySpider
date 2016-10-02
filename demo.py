#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import cookielib
import time
import json
import MySQLdb
import datetime
from multiprocessing.dummy import Pool as ThreadPool
from optparse import OptionParser
# get user info from bilibili.com, then save to MySql database

# python-mysqldb
# mid_max 44570800 2016-09-30

class spider:
    '''
        bilibili spider
    '''
    def __init__(self):
        self.mode = "normal"
        self.step = 2048
        self.sleep = 2
        self.foot_num = 16
        self.mid = 930055
        self.mid_start = 1
        self.mid_max = 60000000
        self.rmsg = True
        self.time_start = time.time()
    
    def datetime_to_timestamp_in_milliseconds(self, d):
        current_milli_time = lambda: int(round(time.time() * 1000))
        return current_milli_time()

    def get_page(self, mid):

        url = "http://space.bilibili.com/ajax/member/GetInfo"
        # url = "https://www.google.com/ncr"
        head = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://space.bilibili.com/933535/',
            'Origin': 'http://space.bilibili.com',
            'Host': 'space.bilibili.com',
            'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        data_2_post = {
            "_": str(self.datetime_to_timestamp_in_milliseconds(datetime.datetime.now())),
            "mid": mid,
        }
        # print mid
        encoded_data = urllib.urlencode(data_2_post)
        request = urllib2.Request(url, data=encoded_data, headers=head)
        try:
            response = urllib2.urlopen(request)
            # print response.read()
            # print res_data_dict
            # print res_data_dict['level_info']['current_level']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print "mid:%s --URL Error %s--" % (mid, e.code)
            if hasattr(e, "reason"):
                print "mid:%s --URL Error %s--" % (mid, e.reason)
        else:    
            res_data_dict = json.loads(response.read())['data']
            if type(res_data_dict) == type({}):
                self.save_2_database(res_data_dict)
            else:
                print "mid:%s [Errno 404] not found!" % mid

    def save_2_database(self, data_dict):
        dd = data_dict
        
        mid = dd['mid']
        name = dd['name']
        sex = dd['sex']
        face = dd['face']
        coins = dd['coins']
        regtime = dd['regtime']
        spacesta = dd['spacesta']
        birthday = dd['birthday']
        place = dd['place']
        description = dd['description']
        article = dd['article']
        attentions = dd['attentions']
        fans = dd['fans']
        friend = dd['friend']
        attention = dd['attention']
        sign = dd['sign']
        li_current_level = dd['level_info']['current_level']
        li_current_min = dd['level_info']['current_min']
        li_current_exp = dd['level_info']['current_exp']
        li_next_exp = dd['level_info']['next_exp']
        pdt_pid = dd['pendant']['pid']
        pdt_name = dd['pendant']['name']
        pdt_expire = dd['pendant']['expire']
        ov_type = dd['official_verify']['type']
        ov_desc = dd['official_verify']['desc']
        theme = dd['theme']
        playNum = dd['playNum']
        # vim :56,74 s/\(\w\+\)/\1 = dd['\1']/g
        try:
            mdb = MySQLdb.connect(host='localhost', user='root', passwd='key', charset='utf8')
            cur = mdb.cursor()
            mdb.select_db('bilibili_users')
            sqlStr = "INSERT INTO bilibili_user_info(\
                        mid,name,sex,face,coins,regtime,spacesta,birthday,place,description,article,attentions,\
                        fans,friend,attention,sign,li_current_level,li_current_min,li_current_exp,li_next_exp,\
                        pdt_pid,pdt_name,pdt_expire,ov_type,ov_desc,theme,playNum\
                        ) \
                     VALUES(\
                        '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                        '%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                        '%s','%s','%s','%s','%s','%s','%s'\
                        )" % (\
                        mid,MySQLdb.escape_string(name),sex,face,coins,regtime,spacesta,birthday,place,MySQLdb.escape_string(description),article,attentions,\
                        fans,friend,attention,MySQLdb.escape_string(sign),li_current_level,li_current_min,li_current_exp,li_next_exp,\
                        pdt_pid,MySQLdb.escape_string(pdt_name),pdt_expire,ov_type,ov_desc,theme,playNum\
                        )
            # print sqlStr
            # print "Execute sql"
            cur.execute(sqlStr)
            # print "Commit"
            mdb.commit()
        except MySQLdb.Error, e:
            mdb.rollback()
            print "mid:%s --Mysql Error %d: %s--" % (mid, e.args[0], e.args[1])
        finally:
            mdb.close()

    def save_cookie(self):

        cookie_container = 'bilibili_cookie'
        cookie = cookielib.MozillaCookieJar(cookie_container)
        # create 'cookie processor'
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        try:
            response = opener.open('http://www.bilibili.com')
            print "OK"
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print "--URL Rrror %s--" % e.code
            if hasattr(e, "reason"):
                print "--URL Error %s--" % e.reason
        else:
            # ignore_discard: save even cookies set to be discarded.
            # ignore_expires: save even cookies that have expiredThe file is overwritten if it already exists
            cookie.save(ignore_discard=True, ignore_expires=True)

    def test(self):
        self.get_page(self.mid)

    def run_test(self):

        mid_max = self.mid_max
        workers = self.foot_num
        mid_start = self.mid_start
        mid_end = mid_start + self.step
        
        if self.step < workers:
            workers = self.step
        print "---------------------------------------------Start----------------------------------------------" 
        while mid_start < mid_max:
            time_step_start = time.time()

            mids = [x for x in range(mid_start, mid_end)]
            
            pool = ThreadPool(workers)
            results = pool.map(self.get_page, mids)
            
            pool.close()
            pool.join()

            if self.rmsg:
                
                time_step_end = time.time()
                data_ps = self.step / (time_step_end - time_step_start)
                avg_data_ps = (mid_end - self.mid_start) / (time_step_end - self.time_start)
                f_progress = (mid_end - self.mid_start) / (self.mid_max * 1.0)
                
                print "#%s>%s" % ('|' * int(f_progress * 100), '-' * int((1- f_progress) * 100))
                print "Time: %s -> %s" % (time_step_start, time_step_end)
                print "Got mid: %s -> %s at speed: %s" % (mid_start, mid_end-1, data_ps)
                print "Average speed: %s" % (avg_data_ps)
                print "Progress: %.4f%%" % (f_progress * 100)
                print "Parameter: -t %s -f %s -p %s" % (self.step, self.foot_num, self.sleep)
                print "#%s>%s" % ('|' * int(f_progress * 100), '-' * int((1- f_progress) * 100))

            mid_start = mid_end
            mid_end = mid_start + self.step

            if self.sleep > 0: 
                time.sleep(self.sleep)


if __name__ == '__main__':

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--mode", action="store",
                        type="string", dest="run_mode", default="normal",
                        help="run mode:[normal, test]")
    parser.add_option("-i", "--mid", action="store",
                        type="int", dest="mid", default=930055,
                        help="-i 930055")
    parser.add_option("-s", "--startmid",
                        type="int", dest="startmid", default=1,
                        help="-s 930055")
    parser.add_option("-t", "--step",
                        type="int", dest="step", default=2048,
                        help="step must >0")
    parser.add_option("-f", "--foot_num",
                        type="int", dest="foot_num", default=16,
                        help="foot_num must >=1")
    parser.add_option("-p", "--sleep",
                        type="int", dest="sleep", default=2)
    parser.add_option("-r", "--rmsg", action="store_false",
                        dest="rmsg", default=True,
                        help="-r: not to print running msg")

    options, args = parser.parse_args()

    print "run_mode:%s" % options.run_mode
    print "print runnins msg: %s" % options.rmsg
    tiny_spider = spider()
    
    if options.run_mode == 'normal':

        if options.step > 0 and options.foot_num > 0:
            print "startmid:%s" % options.startmid
            print "step:%s" % options.step
            tiny_spider.mid_start = options.startmid
            tiny_spider.step = options.step
            tiny_spider.foot_num = options.foot_num
            tiny_spider.sleep = options.sleep
            tiny_spider.rmsg = options.rmsg

            tiny_spider.run_test()

        else:
            parser.print_help()

    elif options.run_mode == 'test':
        print "mid:%s" % options.mid
        tiny_spider.mid = options.mid

        tiny_spider.test()

    else:
        parser.print_help()
    # test()
    #time1 = time.time()
    #run_test()
    # try_con(mid=930909)
    #time2 = time.time()
    #print "Start at:%s End at:%s" % (time1, time2)
