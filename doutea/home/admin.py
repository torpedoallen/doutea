# -*- coding: utf-8 -*-

from django.contrib import admin
from doutea.home.models import *
from django.core import urlresolvers
from django.http import HttpResponseRedirect
import urllib

class CategoryInline(admin.TabularInline):
    model = Category

class DishInline(admin.TabularInline):
    model = Dish

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dish_name', 'memo', 'prop2', 'prop2', 'prop3', 'prop4', 'is_frozen')
    #list_display = ('id', 'name', 'dish_name', 'memo', 'prop1', 'prop2', 'prop3', 'prop4')
    list_display_links = ('name',)
    inlines = [ DishInline, ]

    def response_change(self, request, obj):
        super(CategoryAdmin, self).response_change(request, obj)
        url = urlresolvers.reverse('admin:home_category_changelist')
        params = urllib.urlencode({'vendor__id__exact': obj.vendor_id})
        return HttpResponseRedirect('%s?%s' % (url, params))

class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tel', 'memo', 'admin_view_dishes')
    list_display_links = ('name',)
    inlines = [ CategoryInline, ]

    def admin_view_dishes(self, object):
        url = urlresolvers.reverse('admin:home_category_changelist')
        params = urllib.urlencode({'vendor__id__exact': object.id})
        return '<a href="%s?%s">编辑菜单</a>' % (url, params)

    admin_view_dishes.allow_tags = True
    admin_view_dishes.short_description = "编辑菜单"

class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'prop1', 'prop2', 'prop3', 'prop4')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_nickname', 'admin_avatar', 'admin_home_url')
    list_display_links = ('admin_nickname',)
    fields = ('id', 'nickname', 'avatar_url', 'home_url')
    readonly_fields = ('id', 'nickname', 'avatar_url', 'home_url')

    def admin_nickname(self, object):
        return object.nickname
    admin_nickname.short_description = "昵称"

    def admin_avatar(self, object):
        return '<img src="%s">' % object.avatar_url
    admin_avatar.allow_tags = True
    admin_avatar.short_description = "头像"

    def admin_home_url(self, object):
        return '<a href="%s" target="_blank">%s</a>' % (object.home_url, object.nickname)
    admin_home_url.allow_tags = True
    admin_home_url.short_description = "豆瓣主页"

    admin_nickname.short_description = "昵称"

    def has_add_permission(self, request):
        return False

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
