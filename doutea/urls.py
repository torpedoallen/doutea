# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doutea.views.home', name='home'),
    # url(r'^doutea/', include('doutea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # 注意: 由于订单页面用了首字母为o的url，所以其他url的首字母都不能为o
    url(r'^$', 'doutea.home.views.home'),
    url(r'^login$', 'doutea.home.views.login'),
    url(r'^logout$', 'doutea.home.views.logout'),
    url(r'^mine/?$', 'doutea.home.views.mine'),
    url(r'^do_login$', 'doutea.home.views.do_login'),
    url(r'^authenticated$', 'doutea.home.views.authenticated'),
    url(r'^create_order$', 'doutea.home.views.create_order'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT }), 
    url(r'^favicon.ico$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT, 'path': '/favicon.ico' }),

    url(r'^o(\w+)/?$', 'doutea.home.views.order'),
    url(r'^v(\d+)/?$', 'doutea.home.views.show_vendor'),
    url(r'^d(\d+)/?$', 'doutea.home.views.show_dish'),
    url(r'^d(\d+)/detail?$', 'doutea.home.views.detail_by_dish'),
    url(r'^([vd])(\d+)/add_review/?$', 'doutea.home.views.add_review'),
    url(r'^d(\d+)/rate/?$', 'doutea.home.views.rate'),
    url(r'^o(\w+)/place_order$', 'doutea.home.views.place_order'),
    url(r'^o(\w+)/order_content$', 'doutea.home.views.order_content'),
    url(r'^o(\w+)/delete$', 'doutea.home.views.delete'),
    url(r'^o(\w+)/finish$', 'doutea.home.views.finish'),

#    url(r'^admin/', include('doutea.admin.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
