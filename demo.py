import urllib
import urllib2
import cookielib
import time
import json
import MySQLdb
import datetime
from multiprocessing.dummy import Pool as ThreadPool

# get user info from bilibili.com and save to MySql database

# sudo apt-get install python-mysqldb
# max_mid 44570800 2016-09-30

def datetime_to_timestamp_in_milliseconds(d):
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time()

def get_page(mid):

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
        "_": str(datetime_to_timestamp_in_milliseconds(datetime.datetime.now())),
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
            save_2_database(res_data_dict)
        else:
            print "mid:%s [Errno 404] not found!" % mid

def save_2_database(data_dict):
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
    playNum = dd['playNum']
    # vim :56,74 s/\(\w\+\)/\1 = dd['\1']/g
    try:
        mdb = MySQLdb.connect(host='localhost', user='root', passwd='key', charset='utf8')
        cur = mdb.cursor()
        mdb.select_db('bilibili_users')
        sqlStr = "INSERT INTO bilibili_user_info(\
                 mid,name,sex,face,coins,regtime,spacesta,birthday,place,description,article,attentions,\
                 fans,friend,attention,sign,li_current_level,li_current_min,li_current_exp,li_next_exp,playNum) \
                 VALUES(\
                 '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' \
                 )" % \
                 (mid,name,sex,face,coins,regtime,spacesta,birthday,place,description,article,attentions,\
                 fans,friend,attention,sign,li_current_level,li_current_min,li_current_exp,li_next_exp,playNum)
        # print "Execute sql"
        cur.execute(sqlStr)
        # print "Commit"
        mdb.commit()
    except MySQLdb.Error, e:
        mdb.rollback()
        print "mid:%s --Mysql Error %d: %s--" % (mid, e.args[0], e.args[1])
    finally:
        mdb.close()

def save_cookie():

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
    
def get_newest_mid(min_mid, max_mid=1300000000):
    if try_con(max_mid):
        return max_mid
    else 

def try_con(mid):    
    url = "http://space.bilibili.com/ajax/member/GetInfo"
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        print response.read()
        # print res_data_dict
        # print res_data_dict['level_info']['current_level']
    except urllib2.URLError, e:
        return False
    else:
        return True



def test(mid=930055):
    # mid=930055 is not exist in bilibili databases,
    # this function just for connection test
    get_page(mid)

def run_test():
    # simple test
    mid_start = 930500
    mid_end = 931000
    mids = [x for x in range(mid_start, mid_end)]
    # print mids
    # 4 workers
    pool = ThreadPool(20)
    results = pool.map(get_page, mids)
    # try:
    #     results = pool.map(get_page, mids)
    # except Exception:
    #     print 'ConnectionError'
    #     results = pool.map(get_page, mids)
        
    pool.close()
    pool.join()

if __name__ == '__main__':
    # test()
    run_test()
    # try_con(mid=930909)


