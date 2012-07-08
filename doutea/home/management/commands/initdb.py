# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from home.models import *
from random import randint


class Command(BaseCommand):

    def handle(self, *args, **options):

        vendor = Vendor(name='CoCo都可茶饮', tel='137-1891-1577', memo='6杯起送，满10杯送1杯')
        vendor.save()

        cat = Category(name='冬季限定', vendor=vendor, dish_name='奶茶', prop1='热,去冰,有冰', prop2='全糖,半糖,微糖,无糖')
        cat.save()

        Dish(name='薏仁红豆', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='薏仁燕麦', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='薏仁双拼', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='薏仁牛奶', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='榛果核桃燕麦', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='巧克力燕麦', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='桂圆红枣茶', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='桂圆红枣巧克力', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='白兰地桂圆红枣茶', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='白兰地咖啡', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='白兰地奶茶', category=cat, price=7, rating=randint(0,10)).save()

        cat = Category(name='醇香奶茶', vendor=vendor, dish_name='奶茶', prop1='热,去冰,有冰', prop2='全糖,半糖,微糖,无糖')
        cat.save()

        Dish(name='珍珠奶茶', category=cat, price=6, rating=randint(0,10)).save()
        Dish(name='布丁奶茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='CoCo奶茶', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='椰果奶茶', category=cat, price=6, rating=randint(0,10)).save()
        Dish(name='茉香奶茶', category=cat, price=6, rating=randint(0,10)).save()
        Dish(name='QQ奶茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='双拼奶茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='焦糖奶茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='奶茶三兄弟', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='红豆奶茶', category=cat, price=7, rating=randint(0,10)).save()

        cat = Category(name='醇黑浓情', vendor=vendor, dish_name='奶茶', prop1='热,去冰,有冰', prop2='全糖,半糖,微糖,无糖')
        cat.save()

        Dish(name='CoCo巧克力', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='布丁巧克力', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='双拼巧克力', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='焦糖巧克力', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='焦糖布丁巧克力', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='红豆巧克力', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='CoCo咖啡', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='焦糖咖啡', category=cat, price=9, rating=randint(0,10)).save()

        cat = Category(name='白色恋人', vendor=vendor, dish_name='奶茶', prop1='热,去冰,有冰', prop2='全糖,半糖,微糖,无糖')
        cat.save()

        Dish(name='红茶欧蕾', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='芒果欧蕾', category=cat, prop1='去冰,有冰', price=9, rating=randint(0,10)).save()
        Dish(name='玫瑰盐奶盖绿', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='玫瑰盐奶盖红', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='玫瑰盐芒果奶盖绿', category=cat, prop1='去冰,有冰', price=9, rating=randint(0,10)).save()

        cat = Category(name='果然遇见茶', vendor=vendor, dish_name='奶茶', prop1='热,去冰,有冰', prop2='全糖,半糖,微糖,无糖')
        cat.save()

        Dish(name='金桔柠檬汁', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='鲜柠檬绿茶', category=cat, prop1='去冰,有冰', price=7, rating=randint(0,10)).save()
        Dish(name='鲜柠檬红茶', category=cat, prop1='去冰,有冰', price=7, rating=randint(0,10)).save()
        Dish(name='芒果绿茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='茉莉绿茶', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='QQ绿茶', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='宇治金时', category=cat, prop1='热', price=13, rating=randint(0,10)).save()

        # =============================================================================
        vendor = Vendor(name='东池便当', tel='84564779,84564819', memo='10:00-20:00')
        vendor.save()

        cat = Category(name='东池便当', vendor=vendor, dish_name='便当', prop1='可乐,汤')
        cat.save()

        Dish(name='鸡腿饭', category=cat, price=19, rating=randint(0,10)).save()
        Dish(name='排骨饭', category=cat, price=17, rating=randint(0,10)).save()
        Dish(name='卤肉饭', category=cat, price=17, rating=randint(0,10)).save()
        Dish(name='红烧排骨饭', category=cat, price=17, rating=randint(0,10)).save()
        Dish(name='招牌饭', category=cat, price=15, rating=randint(0,10)).save()
        Dish(name='鲜虾卷饭', category=cat, price=16, rating=randint(0,10)).save()
        Dish(name='鱼排饭', category=cat, price=13, rating=randint(0,10)).save()
        Dish(name='花枝鱼排饭', category=cat, price=14, rating=randint(0,10)).save()
        Dish(name='香肠饭', category=cat, price=15, rating=randint(0,10)).save()
        Dish(name='鸡翅饭', category=cat, price=15, rating=randint(0,10)).save()

        # =============================================================================
        vendor = Vendor(name='九格便当', tel='5722-5064,5745-1115', memo='6份送大桶饮料')
        vendor.save()

        cat = Category(name='便当', vendor=vendor, dish_name='便当')
        cat.save()

        Dish(name='泰式鸡片饭', category=cat, price=19, memo='周一15元', rating=randint(0,10)).save()
        Dish(name='泰式豆腐饭', category=cat, price=16, memo='周一14元', rating=randint(0,10)).save()
        Dish(name='招牌卤肉饭', category=cat, price=17, rating=randint(0,10)).save()
        Dish(name='九格素味', category=cat, price=14, rating=randint(0,10)).save()
        Dish(name='黑椒鸡肉饭', category=cat, price=19, memo='周三16元', rating=randint(0,10)).save()
        Dish(name='鸡排饭', category=cat, price=16, memo='周二14元', rating=randint(0,10)).save()
        Dish(name='烧肉饭', category=cat, price=17, rating=randint(0,10)).save()
        Dish(name='无骨鸡肉饭', category=cat, price=18, memo='周五15元', rating=randint(0,10)).save()
        Dish(name='沙茶滑鸡饭', category=cat, price=18, memo='周四15元', rating=randint(0,10)).save()
        Dish(name='牛肉丸子饭', category=cat, price=18, memo='周三15元', rating=randint(0,10)).save()
        Dish(name='香肠饭', category=cat, price=15, rating=randint(0,10)).save()
        Dish(name='炒烤鸡腿饭(剔骨)', category=cat, price=22, rating=randint(0,10)).save()

        # =============================================================================
        vendor = Vendor(name='桂林米粉', tel='86511179,15101649448', memo='')
        vendor.save()

        cat = Category(name='米粉', vendor=vendor, dish_name='米粉')
        cat.save()

        Dish(name='什锦米粉', category=cat, price=15, rating=randint(0,10)).save()
        Dish(name='红烧排骨米粉', category=cat, price=13, rating=randint(0,10)).save()
        Dish(name='麻辣牛肉米粉', category=cat, price=12, rating=randint(0,10)).save()
        Dish(name='五香牛腩米粉', category=cat, price=12, rating=randint(0,10)).save()
        Dish(name='红烧牛肉米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='牛肚米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='红烧猪脚米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='蜜制叉烧米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='鸡胗米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='鸡肉米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='酸辣笋尖米粉', category=cat, price=11, rating=randint(0,10)).save()
        Dish(name='香菇肉丝米粉', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='榨菜肉丝米粉', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='酸辣豆角米粉', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='卤蛋米粉', category=cat, price=9, rating=randint(0,10)).save()
        Dish(name='贡丸米粉', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='鱼丸米粉', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='牛丸米粉', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='青菜米粉', category=cat, price=7, rating=randint(0,10)).save()

        cat = Category(name='小吃', vendor=vendor, dish_name='小吃')
        cat.save()

        Dish(name='卤鸭腿', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='笋尖', category=cat, price=4, rating=randint(0,10)).save()
        Dish(name='卤蛋', category=cat, price=1, rating=randint(0,10)).save()
        Dish(name='青菜', category=cat, price=4, rating=randint(0,10)).save()
        Dish(name='另加肉类', category=cat, price=10, rating=randint(0,10)).save()
        Dish(name='另加丸类', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='煎蛋', category=cat, price=2, rating=randint(0,10)).save()
        Dish(name='酸豆角', category=cat, price=3, rating=randint(0,10)).save()
        Dish(name='黄豆', category=cat, price=3, rating=randint(0,10)).save()

        cat = Category(name='煲仔', vendor=vendor, dish_name='煲仔饭')
        cat.save()

        Dish(name='青菜煲仔饭', category=cat, price=8, rating=randint(0,10)).save()
        Dish(name='卤鸭腿煲仔饭', category=cat, price=12, rating=randint(0,10)).save()
        Dish(name='香菇鸡肉煲仔饭', category=cat, price=12, rating=randint(0,10)).save()
        Dish(name='广式腊味煲仔饭', category=cat, price=12, rating=randint(0,10)).save()
        Dish(name='牛腩煲仔饭', category=cat, price=15, rating=randint(0,10)).save()
        Dish(name='排骨煲仔饭', category=cat, price=15, rating=randint(0,10)).save()

        cat = Category(name='四季甜品', vendor=vendor, dish_name='甜品', memo='龟苓膏配一种5元，两种6元，三种7元')
        cat.save()

        Dish(name='炼奶龟苓膏', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='什果龟苓膏', category=cat, price=7, rating=randint(0,10)).save()
        Dish(name='蜂蜜龟苓膏', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='凤梨龟苓膏', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='芒果龟苓膏', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='草莓龟苓膏', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='绿豆马蹄爽', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='红豆沙', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='银耳莲子羹', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='凤梨西米露', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='芒果西米露', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='草莓西米露', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='情人果西米露', category=cat, price=5, rating=randint(0,10)).save()
        Dish(name='红枣西米露', category=cat, price=5, rating=randint(0,10)).save()
