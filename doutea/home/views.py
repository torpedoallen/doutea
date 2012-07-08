# Create your views here.
# -*- coding: utf-8 -*-

from itertools import groupby
import hashlib
import random
import time
import django.utils.simplejson as json
from collections import defaultdict
from datetime import date, datetime, timedelta
from doutea.home.models import *
from doutea.home.oauth2 import douban
from djangomako.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.db import connection
from django.conf import settings
from django.db.models import Q

def generate_label():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    seed = random.randint(0, int(time.mktime(datetime.now().timetuple())))
    m = hashlib.md5()
    m.update(str(seed))
    seed = m.hexdigest()

    return ''.join( chars[int(seed[i*4:i*4+4], 16) % 62] for i in range(8) )


def require_login(func):
    def _(request, *a, **kw):
        from django.contrib.auth import SESSION_KEY
        invalid_session = False
        if SESSION_KEY in request.session:
            try:
                user_id = request.session[SESSION_KEY]
                user = User.objects.get(id=user_id)
                request.user = user
            except User.DoesNotExist:
                invalid_session = True
        else:
            invalid_session = True

        if invalid_session:
            resp = HttpResponseRedirect('/login')
            resp.set_cookie('redir', request.path)
            return resp
        return func(request, *a, **kw)
    _.__name__ = func.__name__
    _.__doc__ = func.__doc__
    _.__dict__.update(func.__dict__)
    return _

def create_context(request, **kwargs):
    context = {
        'system_name': settings.SYSTEM_NAME,
    }

    if isinstance(request.user, User):
        context.update({
            'user': request.user,
        })

    context.update(kwargs)

    return context

@require_login
def home(request):

    today = date.today()
    order_items = OrderItem.objects.filter(user=request.user.id, create_time__gt=today - timedelta(days=3))
    order_ids = list(set(order_item.order_id for order_item in order_items))
    orders = Order.objects.select_related('vendor', 'creator').filter((Q(id__in=order_ids) | Q(creator=request.user.id)) & Q(create_time__gt=today - timedelta(days=3)))
    vendors = Vendor.objects.all()
    today_orders = []
    previous_orders = []

    for order in orders:
        if order.create_time.date() == today:
            today_orders.append(order)
        else:
            previous_orders.append(order)

    context = create_context(request,
         today=date.today().isoformat(),
         today_orders=today_orders,
         previous_orders=previous_orders,
         vendors=vendors,
         orders=[],
    )
    return render_to_response('home/home.html', context)


@require_login
def mine(request):

    orderitems = OrderItem.objects.select_related('dish__vendor__category').filter(user=request.user.id).order_by('-create_time')
    context = create_context(request,
        orderitems=orderitems,
    )
    return render_to_response('/home/mine.html', context)


@require_login
def order(request, label):

    try:
        order = Order.objects.select_related('vendor', 'creator').get(label=label)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Not Found")

    finished = (order.finished == 'y')

    deadline_timestamp = int(time.mktime(order.deadline.timetuple()))

    order_items = OrderItem.objects.select_related('dish').filter(order=order.id)
    order_stat = { 'total_items': len(order_items), 'total_price': 0, 'items': {}}
    for item in order_items:
        key = ','.join((item.dish.name, item.props()))
        order_stat['items'].setdefault(key, {'dish_id':item.dish_id, 'count': 0})['count'] += 1
        order_stat['total_price'] += item.dish.price


    # 菜单
    dish_data = defaultdict(list)
    dishes = Dish.objects.select_related('category').filter(category__vendor=order.vendor_id, \
                                                            category__is_frozen=False)
    #dishes = Dish.objects.select_related('category').filter(category__vendor=order.vendor_id)
    for dish in dishes:
        dish_data[dish.category.name].append(dish)

    # 默认值
    if not order.item_limit:
        order.item_limit = 100

    context = create_context(request,
        dishes=dict(dish_data),
        order_stat=order_stat,
        order=order,
        deadline=deadline_timestamp,
        finished=finished,
    )

    return render_to_response('home/order.html', context)

@require_login
def order_content(self, label):

    try:
        order = Order.objects.get(label=label)

        order_items = OrderItem.objects.select_related('user', 'dish').filter(order=order.id)

        d = {}
        for order_item in order_items:
            d.setdefault(order_item.user.nickname, {
                'total_price': 0,
                'user_id': order_item.user.id,
                'nickname': order_item.user.nickname,
                'home_url': order_item.user.home_url,
                'items': [],
            })['items'].append({
                'id': order_item.id,
                'dish_name': order_item.dish.name,
                'props': order_item.props(),
                'price': order_item.dish.price,
            });

        for v in d.values():
            v['items'].sort(key=lambda x:(x['dish_name'], x['props']))
            v['total_price'] = sum(item['price'] for item in v['items'])

        order_content = {
            'total_users': len(d),
            'total_price': sum(v['total_price'] for v in d.values()),
            'total_items': sum(len(v['items']) for v in d.values()),
            'users': d,
        }

        return HttpResponse(json.dumps(order_content))
    except Order.DoesNotExist, OrderItem.DoesNotExist:
        return HttpResponseNotFound('Not Found')

def login(request):
    return render_to_response('home/login.html', create_context(request))

def do_login(request):
    url = douban.login()
    return HttpResponseRedirect(url)

def authenticated(request):
    code = request.GET.get('code')
    result = douban.authenticated(code)

    douban_user_id = result['douban_user_id']
    try:
        user = User.objects.get(id=douban_user_id)
    except User.DoesNotExist:
        user = User(id=douban_user_id)
    user.access_token=result['access_token']
    user.save()

    from django.contrib.auth import SESSION_KEY
    request.session.set_expiry(datetime.now() + timedelta(days=30))
    request.session[SESSION_KEY] = douban_user_id

    # 更新用户信息
    result = douban.user_info(user.access_token)

    if result:
        user.nickname = result['title']['$t']
        for link in result['link']:
            if link['@rel'] == 'icon':
                user.avatar_url = link['@href']
            elif link['@rel'] == 'alternate':
                user.home_url = link['@href']

        user.save()

    redir = request.COOKIES.get('redir', '')

    return HttpResponseRedirect(redir if redir else '/')


def logout(request):
    from django.contrib.auth import SESSION_KEY
    del request.session[SESSION_KEY]
    return HttpResponseRedirect('/')


@require_login
def create_order(request):
    user = request.user

    errors = []

    save = request.POST.get('save', '')

    if save:
        label = generate_label()

        # 处理结束时间
        now = datetime.now()
        deadline_type = request.POST.get('deadline_type', 'length')
        if deadline_type == 'time':
            deadline_hour = int(request.POST.get('hour', now.hour + 1))
            deadline_minute = int(request.POST.get('minute', 0))
            deadline = datetime(now.year, now.month, now.day, deadline_hour, deadline_minute)
            if deadline < now:
                deadline = deadline + timedelta(days=1)
        else:
            finish_in = request.POST.get('finish_in', '60')
            if not finish_in.isdigit():
                finish_in = 60
            else:
                finish_in = int(finish_in)
            deadline = now + timedelta(minutes=finish_in)

        # 数量限制
        item_limit = request.POST.get('item_limit', '100')
        if item_limit.isdigit():
            item_limit = int(item_limit)
        else:
            item_limit = 100            # 默认值

        # 餐厅
        vendor_id = request.POST.get('vendor_id', '0')
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            order = Order(creator=user, label=label, vendor=vendor, create_time=datetime.now(), deadline=deadline, finished='n', item_limit=item_limit)
            order.save()

            return HttpResponseRedirect('/o%s/' % order.label)

        except Vendor.DoesNotExist:
            errors = ['请选择一家餐厅。']

    # 显示表单
    vendors = Vendor.objects.all()
    now = datetime.now()
    if now.minute >= 30:
        deadline_hour = now.hour + 2
        deadline_minute = '00'
    else:
        deadline_hour = now.hour + 1
        deadline_minute = '30'

    if deadline_hour >= 24:
        deadline_hour -= 24

    context = create_context(request,
        vendors=vendors,
        deadline_minute=deadline_minute,
        deadline_hour=deadline_hour,
        errors=errors,
    )
    return render_to_response('home/create_order.html', context)

@require_login
def place_order(request, label):
    from django.db.models import Count
    user = request.user
    order_label = request.POST.get('request_label', '')
    dish_id = request.POST.get('id', '');
    prop1 = request.POST.get('prop1', '');
    prop2 = request.POST.get('prop2', '');
    prop3 = request.POST.get('prop3', '');
    prop4 = request.POST.get('prop4', '');

    try:
        result = None
        order = Order.objects.get(label=label)
        if not order.item_limit:
            order.item_limit = 100
        if order.finished == 'y':
            result = { 'result': 'error', 'error': '该订单已结束' }
        else:
            # 查一下现有订单数量有没有超出限额
            existing_order_items = OrderItem.objects.filter(order=order.id)

            if len(existing_order_items) > order.item_limit:
                # 超出的话，只有已参团的人才能继续订
                if user.id not in [ order_item.user_id for order_item in existing_order_items ]:
                    result = { 'result': 'error', 'error': '该订单已达到上限，不能再下单' }

        if not result:
            dish = Dish.objects.get(id=dish_id)
            order_item = OrderItem(order_id=order.id, user_id=user.id, dish_id=dish.id, prop1=prop1, prop2=prop2, prop3=prop3, prop4=prop4, create_time=datetime.now())
            order_item.save()
            result = { 'result': 'ok' }

        return HttpResponse(json.dumps(result))
    except Order.DoesNotExist:
        return HttpResponseNotFound('Not Found')

@require_login
def delete(request, label):
    try:
        result = None

        order = Order.objects.get(label=label)
        if order.finished == 'y':
            result = {"result":"error","error":"该订单已结束"}
        else:
            order_item_id = request.GET.get('id', '')
            order_item = OrderItem.objects.get(id=order_item_id)
            if order_item.order_id != order.id:

                result = {"result":"error","error":"你无权删除该订单项"}
        if not result:
            order_item.delete()
            result = {"result": "ok"}

        return HttpResponse(json.dumps(result))
    except (Order.DoesNotExist, OrderItem.DoesNotExist):
        return HttpResponseNotFound('Not Found')


@require_login
def finish(request, label):

    try:
        order = Order.objects.get(label=label)
        order.finished = 'y'
        order.save()
        return HttpResponseRedirect('/o%s/' % order.label)
    except Order.DoesNotExist:
        return HttpResponseNotFound('Not Found')


@require_login
def show_vendor(request, id):
    try:
        vendor = Vendor.objects.get(id=id)
        context = create_context(request, vendor=vendor)
        return render_to_response('home/show_vendor.html', context)
    except Vendor.DoesNotExist:
        return HttpResponseNotFound('Not Found')


@require_login
def show_dish(request, id):
    try:
        dish = Dish.objects.get(id=id)
        try:
            rating = Rating.objects.get(user=request.user.id, dish_id=dish.id)
            myrating = rating.rating
        except Rating.DoesNotExist:
            myrating = 0

        context = create_context(request, dish=dish, myrating=myrating)
        return render_to_response('home/show_dish.html', context)
    except Dish.DoesNotExist:
        return HttpResponseNotFound('Not Found')


@require_login
def add_review(request, cat, subject_id):

    subject = None
    try:
        if cat == 'd':
            cat_id = DISH_CAT_ID
            subject = Dish.objects.get(id=subject_id)
        elif cat == 'v':
            cat_id = VENDOR_CAT_ID
            subject = Vendor.objects.get(id=subject_id)
        else:
            return HttpResponseNotFound('Not Found')
    except Vendor.DoesNotExist, Dish.DoesNotExist:
        return HttpResponseNotFound('Not Found')


    save = request.POST.get('save', '')
    error = ''
    if save:
        content = request.POST.get('content', '')

        if not content:
            error = u'请输入评论内容。'
        else:
            review = Review(
                user=request.user,
                content=content,
                update_time=datetime.now(),
                subject_id=subject_id,
                cat_id=cat_id,
            )
            review.save()
            return HttpResponseRedirect('/%s%s/' % (cat, subject_id))

    context = create_context(request, cat_id=cat_id, subject=subject, error=error)
    return render_to_response('home/add_review.html', context)


@require_login
def rate(request, dish_id):
    rating_value = request.POST.get('rating', '')
    comment = request.POST.get('comment', '')

    try:
        dish = Dish.objects.get(id=dish_id)
    except Dish.DoesNotExist:
        return HttpResponseNotFound('Not Found')

    if rating_value.isdigit() and int(rating_value) > 0 and int(rating_value) <= 10:
        rating_value = int(rating_value)

        try:
            rating = Rating.objects.get(user=request.user, dish_id=dish.id)
        except Rating.DoesNotExist:
            rating = Rating(user=request.user, dish_id=dish.id)

        rating.rating = rating_value
        rating.comment = comment
        rating.update_time = datetime.now()
        rating.save()

        # 计算被评价的dish的评价人数和平均分数
        ratings = Rating.objects.filter(dish_id=dish.id)
        rating_count = len(ratings)
        avergage_rating = int(round(sum( r.rating for r in ratings) / rating_count)) if rating_count > 0 else 0
        dish.rating = avergage_rating
        dish.rating_count=rating_count
        dish.save()

        result = { 'result': 'ok' }
    else:
        result = { 'result': 'error' }

    return HttpResponse(json.dumps(result))


@require_login
def detail_by_dish(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except Dish.DoesNotExist:
        return HttpResponseNotFound('Not Found')

    ratings = Rating.objects.filter(dish_id=dish.id).order_by('-update_time')

    result = {
        'dish': {
            'id': dish.id,
            'name': dish.name,
            'rating': dish.rating,
            'rating_count': dish.rating_count,
            'ratings': [ {
                'user': {
                    'id': rating.user.id,
                    'nickname': rating.user.nickname,
                    'avatar_url': rating.user.avatar_url,
                    'home_url': rating.user.home_url,
                },
                'rating': rating.rating,
                'comment': rating.comment,
                'update_time': str(rating.update_time),
            } for rating in ratings ],
        }
    }

    return HttpResponse(json.dumps(result))

