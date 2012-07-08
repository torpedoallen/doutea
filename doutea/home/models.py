# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

VENDOR_CAT_ID = 1
DISH_CAT_ID = 2

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    access_token = models.CharField(max_length=64)
    nickname = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)
    home_url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nickname

class Vendor(models.Model):
    name = models.CharField(max_length=64)          # 店铺名
    tel = models.CharField(max_length=255)          # 电话号码，用,分隔多个号码
    memo = models.CharField(max_length=255)         # 备注

    def __unicode__(self):
        return self.name

    def categories(self):
        return Category.objects.filter(vendor=self)

    def reviews(self):
        return Review.objects.filter(cat_id=VENDOR_CAT_ID, subject_id=self.id)

class Category(models.Model):
    name = models.CharField(max_length=64)          # 分类名
    vendor = models.ForeignKey(Vendor)
    dish_name = models.CharField(max_length=64)     # 菜品类别(如：奶茶，便当，煲仔饭，米粉等)
    memo = models.CharField(max_length=255, blank=True)
    prop1 = models.CharField(max_length=255, blank=True)        # 默认属性1
    prop2 = models.CharField(max_length=255, blank=True)        # 默认属性2
    prop3 = models.CharField(max_length=255, blank=True)        # 默认属性3
    prop4 = models.CharField(max_length=255, blank=True)        # 默认属性4
    is_frozen = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def dishes(self):
        return Dish.objects.filter(category=self)

class Dish(models.Model):
    name = models.CharField(max_length=100)         # 菜品名称
    category = models.ForeignKey(Category)          # 分类id
    price = models.DecimalField(max_digits=12, decimal_places=2)                   # 价格
    memo = models.CharField(max_length=255, blank=True)         # 备注
    prop1 = models.CharField(max_length=255, blank=True)        # 属性1
    prop2 = models.CharField(max_length=255, blank=True)        # 属性2
    prop3 = models.CharField(max_length=255, blank=True)        # 属性3
    prop4 = models.CharField(max_length=255, blank=True)        # 属性4
    rating = models.IntegerField(default=0)                  # 评分，1-10
    rating_count = models.IntegerField(default=0)            # 评分的人数

    def __unicode__(self):
        return self.name

    def props(self):
        result = []
        for i in range(1, 5):
            prop_str = ''
            attrname = 'prop%s' % i
            if hasattr(self, attrname):
                prop_str = getattr(self, attrname)
                if not prop_str:
                    prop_str = getattr(self.category, attrname)
            if not prop_str:
                break
            result.append((attrname, filter(None, prop_str.split(','))))

        return result

    def reviews(self):
        return Review.objects.filter(cat_id=DISH_CAT_ID, subject_id=self.id)

class Order(models.Model):
    label = models.CharField(max_length=8)
    vendor = models.ForeignKey(Vendor)              # 店铺
    creator = models.ForeignKey(User)
    create_time = models.DateTimeField()
    deadline = models.DateTimeField()
    item_limit = models.IntegerField(default=100)              # 订单的数量限制
    finished = models.CharField(max_length=1)

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    user = models.ForeignKey(User)
    dish = models.ForeignKey(Dish)
    prop1 = models.CharField(max_length=255)        # 属性1
    prop2 = models.CharField(max_length=255)        # 属性2
    prop3 = models.CharField(max_length=255)        # 属性3
    prop4 = models.CharField(max_length=255)        # 属性4
    create_time = models.DateTimeField()

    def props(self):
        return ','.join(filter(None, [ self.prop1, self.prop2, self.prop3, self.prop4 ]))


class Review(models.Model):
    cat_id = models.IntegerField()                  # 类别
    subject_id = models.IntegerField()              # 所属餐厅/餐品id
    user = models.ForeignKey(User)
    update_time = models.DateTimeField()            # 发表/更新时间
    content = models.TextField()                    # 内容


class Rating(models.Model):
    user = models.ForeignKey(User)
    dish_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField()
    update_time = models.DateTimeField()            # 评论更新时间


