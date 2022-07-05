"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path

#from blog.views import post_list,post_detail
from blog.views import (
    IndexView,CategoryView,TagView,
    PostDetailView,SearchView,AuthorView
)
from config.views import LinkListView
from .custom_site import custom_site

from comment.views import CommentView

from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from django.contrib.sitemaps import views as sitemap_views
#class view
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('category/<str:category_id>/',CategoryView.as_view(),name='category-list'),
    re_path('tag/(?P<tag_id>\d+)/',TagView.as_view(),name='tag-list'),
    re_path('post/(?P<post_id>\d+).html',PostDetailView.as_view(),name='post-detail'),
    path('super_admin/', admin.site.urls,name='super-admin'),
    path('admin/',custom_site.urls,name='admin'),
    path('search/',SearchView.as_view(),name='search'),
    path('author/<str:owner_id>/',AuthorView.as_view(),name='author'),
    path('links/',LinkListView.as_view(),name='links'),
    path('comment/',CommentView.as_view(),name='comment'),
    #rss或feed
    re_path('rss|feed/',LatestPostFeed(),name='rss'),
    re_path('sitemap\.xml',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
]
'''Function View
urlpatterns = [
	path('',post_list),
	path('category/<str:category_id>/',post_list),
	re_path('tag/(?P<tag_id>\d+)/',post_list),
	re_path('post/(?P<post_id>\d+).html',post_detail),
	path('links/',links),
    path('super_admin/', admin.site.urls),
    path('admin/',custom_site.urls),
]'''

'''当前配置的路由可以创建一些路由映射关系：

/admin/
/admin/login/
/admin/logout/
/admin/password_change/
/admin/password_change/done/

/admin/app名称/model名称/
/admin/app名称/model名称/add/
/admin/app名称/model名称/ID值/history/
/admin/app名称/model名称/ID值/change/
/admin/app名称/model名称/ID值/delete/

 '''