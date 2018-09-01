#coding=utf-8
import MySQLdb, pymongo

#根据关键字，日期，顺序筛选新闻
def get_itnews(keyword, date_start, date_end, order, comment_num):
    myorder = ('asc' if order==1 else 'desc')
    db = MySQLdb.connect("localhost", "test", "123456", "spider_datas", charset='utf8')
    cursor = db.cursor()
    cursor.execute("select title, link, view, comment, posttime from itnews_test where title regexp '%s' and posttime >= '%s' and posttime <= '%s' and comment >= %d order by posttime %s" % (keyword, date_start, date_end, comment_num, myorder))
    datas = cursor.fetchall()
    infos = []
    for data in datas:
        info = {}
        info['title'] = data[0]
        info['link'] = data[1]
        info['view'] = data[2]
        info['comment'] = data[3]
        info['posttime'] = data[4]
        info['post'] = "<span class='news_posttime'>发布时间:" + str(info['posttime']) + "&ensp;&ensp;&ensp;</span>" + "<span class='comment_num' title='评论'>" + str(info['comment']) + "</span>" + "<span><a class='news_title itnews_color' target='_blank' href='" + info['link'] + "'>" + info['title'] + "</a></span><br/>"
        infos.append(info)
    return infos

#根据关键字，日期，顺序筛选新闻
def get_sinanews(keyword, date_start, date_end, order, comment_num):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['spider']
    mycol = mydb['sinanews']
    datas = mycol.find({'title':{'$regex':'%s'%keyword}, 'posttime':{'$gte':date_start, '$lte':date_end}, 'comment_show':{'$gte':comment_num}}, {'title':1, '_id':0, 'url':1, 'posttime':1, 'comment_show':1}).sort('posttime', order)
    infos = []
    for data in datas:
        info = {}
        #info['post'] =  "<span style='font-size:80%;color:#222222'>发布时间:" + data['posttime'] + "&ensp;&ensp;&ensp;&ensp;</span>" + "<span><a style='font-size:100%;color:#ff00cc' target='_blank' href='" + data['url'] + "'>" + data['title'] + "</a></span><br/>"
        info['post'] =  "<span class='news_posttime'>发布时间:" + data['posttime'] + "&ensp;&ensp;&ensp;</span>" + "<span class='comment_num' title='评论'>" + str(data['comment_show']) + "</span>" + "<span><a class='news_title sinanews_color' target='_blank' href='" + data['url'] + "'>" + data['title'] + "</a></span><br/>"
        infos.append(info)
    return infos

#根据关键字，日期，顺序筛选新闻
def get_tencentnews(keyword, date_start, date_end, order, comment_num):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['spider']
    mycol = mydb['tencentnews']
    datas = mycol.find({'$or':[{'title':{'$regex':'%s'%keyword}},{'intro':{'$regex':'%s'%keyword}}], 'publish_time':{'$gte':date_start, '$lte':date_end}, 'comment_num':{'$gte':comment_num}}, {'title':1, '_id':0, 'vurl':1, 'publish_time':1, 'comment_num':1}).sort('publish_time', order)
    #datas = mycol.find({'title':{'$regex':'拼多多'}}, {'title':1, '_id':0, 'url':1, 'publish_time':1}).sort('publish_time', order)
    infos = []
    for data in datas:
        info = {}
        info['post'] =  "<span class='news_posttime'>发布时间:" + data['publish_time'] + "&ensp;&ensp;&ensp;</span>" + "<span class='comment_num' title='评论'>" + str(data['comment_num']) + "</span>" + "<span><a class='news_title tencentnews_color' target='_blank' href='" + data['vurl'] + "'>" + data['title'] + "</a></span><br/>"
        infos.append(info)
    return infos

#根据news_type返回所选择类型的新闻信息
def get_infos(keyword, date_start, date_end, news_type, order, comment_num):
    infos = {'itnews': [], 'sinanews': [], 'tencentnews':[]}
    if news_type=='itnews' or news_type=='all':
        infos['itnews'] = get_itnews(keyword, date_start, date_end, order, comment_num)
    if news_type=='sinanews' or news_type=='all':
        infos['sinanews'] = get_sinanews(keyword, date_start, date_end, order, comment_num)
    if news_type=='tencentnews' or news_type=='all':
        infos['tencentnews'] = get_tencentnews(keyword, date_start, date_end, order, comment_num)
    return infos


if __name__ == '__main__':
    infos = get_infos('火星', '2018-05-01', '2020-01-01', 'all', 1)
    for info in infos['itnews']:
        print(info['title'], info['link'])
#        print(info['post'])
