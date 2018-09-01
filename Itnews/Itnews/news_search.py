# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from . import get_itnews_data, picture_list
import random

# 接收POST请求数据
def search_post(request):
    ctx ={}
    if request.POST:
        ctx['bgp_type'] = request.POST.get('bgp', None)
        ctx['bgp'] = ( random.choice(picture_list.piclist) if ctx['bgp_type']=='random_bgp' else 'i/bgp5.jpg' )
        ctx['bgp_tr'] = (0.5 if ctx['bgp_type']=='random_bgp' else 0.18)
        ctx['keyword'] = ( request.POST.get('keyword', None) if request.POST.get('keyword', None) else '.*' )
        ctx['order'] = (1 if request.POST.get('sort_type', None)=='asc' else -1)
        ctx['news_type'] = request.POST.get('news_type', None)
        ctx['date_start'] = request.POST.get('date_start', None)
        ctx['date_end'] = request.POST.get('date_end', None)
        ctx['comment_num'] = ( request.POST.get('comment_num', None) if request.POST.get('comment_num', None) else 0 )
        infos = get_itnews_data.get_infos(ctx['keyword'], ctx['date_start'], ctx['date_end'], ctx['news_type'], ctx['order'], int(ctx['comment_num']))
        ctx['itnews_posts'] = []
        ctx['sinanews_posts'] = []
        ctx['tencentnews_posts'] = []
        for info in infos['itnews']:
                ctx['itnews_posts'].append(info['post'])
        for info in infos['sinanews']:
                ctx['sinanews_posts'].append(info['post'])
        for info in infos['tencentnews']:
                ctx['tencentnews_posts'].append(info['post'])
        ctx['rlt'] = ctx['keyword'] + '的搜索结果, ' + '共%d条。' % (len(ctx['itnews_posts'])+len(ctx['sinanews_posts'])+len(ctx['tencentnews_posts']))
        return render(request, "post.html", ctx)

    return render(request, "mysite.html", ctx)
