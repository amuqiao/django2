# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('df_user.urls')),
    url(r'^', include('df_goods.urls')),
    # 富文本编辑器
    url(r'^tinymce/', include('tinymce.urls')),
]
