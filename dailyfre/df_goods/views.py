# coding=utf-8
from django.shortcuts import render
from models import *
# Create your views here.


def index(request):
    """
    网站首页 商品页
    实时显示:热销商品 最新商品
    """
    # 啥意思?
    typelist = TypeInfo.objects.all()
    list = []
    for type in typelist:
        list.append({
            'type': type,
            'click_list': type.goodsinfo_set.order_by('-gclick')[0:3],
            'new_list': type.goodsinfo_set.order_by('-id')[0:4]
        })
    context = {'title': '首页', 'list': list}
    return render(request, 'df_goods/index.html', context)

