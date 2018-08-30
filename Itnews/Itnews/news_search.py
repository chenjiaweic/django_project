# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf
from . import get_itnews_data
 
# 接收POST请求数据
def search_post(request):
    ctx ={}
    if request.POST:
        if len(request.POST['keyword']) < 1:
            keyword = '.*'
        else:
            keyword = request.POST['keyword']
        order = (1 if request.POST.get('sort_type', None)=='asc' else -1)
        news_type = request.POST.get('news_type', None)
        ctx['keyword'] = keyword
        ctx['order'] = order
        ctx['news_type'] = news_type
        date_start = request.POST.get('date_start', None)
        date_end = request.POST.get('date_end', None)
        ctx['date_start'] = date_start
        ctx['date_end'] = date_end
        print('date_s', date_start, 'date_e', date_end)
        infos = get_itnews_data.get_infos(keyword, date_start, date_end, news_type, order)
        ctx['posts'] = []
        for info in infos:
                ctx['posts'].append(info['post'])
        ctx['rlt'] = keyword + '的搜索结果, ' + '共%d条。'%len(ctx['posts'])

    return render(request, "post.html", ctx)

