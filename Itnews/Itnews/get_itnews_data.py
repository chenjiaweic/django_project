#coding=utf-8
import MySQLdb, pymongo

#根据关键字，日期，顺序筛选新闻
def get_itnews(keyword, date_start, date_end, order):
    myorder = ('asc' if order==1 else 'desc')
    db = MySQLdb.connect("localhost", "test", "123456", "spider_datas", charset='utf8')
    cursor = db.cursor()
    cursor.execute("select title, link, view, comment, posttime from itnews_test where title regexp '%s' and posttime >= '%s' and posttime <= '%s' order by posttime %s" % (keyword, date_start, date_end, myorder))
    datas = cursor.fetchall()
    infos = []
    for data in datas:
        info = {}
        info['title'] = data[0]
        info['link'] = data[1]
        info['view'] = data[2]
        info['comment'] = data[3]
        info['posttime'] = data[4]
        info['post'] = "<span style='font-size:80%;color:#222222'>发布时间:" + str(info['posttime']) + "&ensp;&ensp;&ensp;&ensp;</span>" + "<span><a target='_blank' href='" + info['link'] + "'>" + info['title'] + "</a></span><br/>"
        infos.append(info)
    return infos

#根据关键字，日期，顺序筛选新闻
def get_sinanews(keyword, date_start, date_end, order):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['spider']
    mycol = mydb['sinanews']
    datas = mycol.find({'title':{'$regex':'%s'%keyword}, 'posttime':{'$gte':date_start, '$lte':date_end}}, {'title':1, '_id':0, 'url':1, 'posttime':1}).sort('posttime', order)
    infos = []
    for data in datas:
        info = {}
        info['post'] =  "<span style='font-size:80%;color:#222222'>发布时间:" + data['posttime'] + "&ensp;&ensp;&ensp;&ensp;</span>" + "<span><a target='_blank' href='" + data['url'] + "'>" + data['title'] + "</a></span><br/>"
        infos.append(info)
    return infos

#根据news_type返回所选择类型的新闻信息
def get_infos(keyword, date_start, date_end, news_type, order):
    infos = {'itnews': [], 'sinanews': []}
    if news_type=='itnews' or news_type=='all':
        infos['itnews'] = get_itnews(keyword, date_start, date_end, order)
    if news_type=='sinanews' or news_type=='all':
        infos['sinanews'] = get_sinanews(keyword, date_start, date_end, order)
    return infos


#if __name__ == '__main__':
#    infos = get_infos('火星', '2018-05-01', '2020-01-01', 'all', 1)
#    for info in infos:
#        print(info['title'], info['link'])
#        print(info['post'])
#    get_sinanews('火星', '2011-01-01', '2020-01-01')
