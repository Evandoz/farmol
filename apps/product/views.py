# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.core import serializers
from django.db.models import F

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, CatalogCategory, Catalog

from operation.models import UserFavorite, UserOrder, UserOrderTable, UserAddress, UserCart

from utils.mixin_utils import LoginRequireMixin

# Create your views here.

class IndexView(View):
	def get(self, request):

		if request.user.is_authenticated():
			carts = UserCart.objects.filter(user=request.user)
			carts_nums = carts.count()

			all_price = 0
			for cart in carts:
				all_price += cart.product.price * cart.count

			carts = carts[:3]
		else:
			carts = None
			carts_nums = 0
			all_price = 0

		fruits = Product.objects.filter(category__catalog__name=u'有机水果')[:3]
		vegetables = Product.objects.filter(category__catalog__name=u'有机蔬菜')[:3]
		dried_fruits = Product.objects.filter(category__catalog__name=u'有机果脯')[:3]
		juices = Product.objects.filter(category__catalog__name=u'有机果汁')[:3]

		return render (request, 'index.html', {
		    'carts': carts,
		    'carts_nums': carts_nums,
		    'fruits': fruits,
		    'vegetables': vegetables,
		    'dried_fruits': dried_fruits,
		    'juices': juices,
		    'all_price': all_price
		})

class ShopView(View):
	def get(self, request):

		if request.user.is_authenticated():
			carts = UserCart.objects.filter(user=request.user)
			carts_nums = carts.count()

			all_price = 0
			for cart in carts:
				all_price += cart.product.price * cart.count

			carts = carts[:3]
		else:
			carts_nums = 0
			all_price = 0
			carts = None

		all_products = Product.objects.all()



		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_products, 12, request=request)
		products = p.page(page)

		return render(request, 'shop.html', {
		    'carts': carts,
		    'carts_nums': carts_nums,
		    'products': products,
		    'all_price': all_price
		})

class DetailView(View):
	def get(self, request):
		product_id = request.GET.get('product_id', 0)

		product = serializers.serialize('json', Product.objects.filter(id=int(product_id)))

		return HttpResponse(product, content_type='application/json')

class AddCartView(View):
	def post(self, request):
		pro_id = request.POST.get('pro_id', 0)
		pro_nums = request.POST.get('pro_nums', 0)

		product = Product.objects.get(id=int(pro_id))

		if not request.user.is_authenticated():
			# 判断用户是否登录、
			return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

		exist_records = UserCart.objects.filter(user=request.user, product=product)

		if exist_records:
			exist_records.update(count=F('count')+pro_nums)

			return HttpResponse('{"status":"success", "msg":"已添加购物车"}', content_type='application/json')

		else:
			if int(pro_id) > 0 and int(pro_nums) > 0:
				new_records = UserCart()
				new_records.user = request.user
				new_records.product = product
				new_records.count = int(pro_nums)

				new_records.save()

				return HttpResponse('{"status":"success", "msg":"已添加购物车"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail", "msg":"添加购物车出错"}', content_type='application/json')

class UpdateCartView(View):
	def post(self, request):
		pro_id = request.POST.get('pro_id', 0)
		pro_nums = request.POST.get('pro_nums', 0)

		product = Product.objects.get(id=int(pro_id))

		exist_records = UserCart.objects.filter(user=request.user, product=product)

		if exist_records:
			exist_records.update(count=pro_nums)

			return HttpResponse('{"status":"success", "msg":"已更新"}', content_type='application/json')

		else:
			return HttpResponse('{"status":"fail", "msg":"更新出错"}', content_type='application/json')

class DeleteCartView(View):
	def post(self, request):
		cart_id = request.POST.get('cart_id', 0)
		cart = UserCart.objects.get(id=int(cart_id))

		if cart:
			cart.delete()
			return HttpResponse('{"status":"success", "msg":"已删除"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail", "msg":"删除出错"}', content_type='application/json')

class ShowOrderView(LoginRequireMixin, View):
	def get(self, request):
		neworder = UserOrderTable.objects.filter(user=request.user, status=1).latest('add_time')

		return render(request, 'order.html', {
		    'neworder': neworder
		})

class GenerateOrderView(LoginRequireMixin, View):
	def post(self, request):
		cartid = request.POST.get('carts_id', u'')

		all_prices = request.POST.get('all_prices', 0)

		orderids = cartid.split(',')

		address = UserAddress.objects.filter(user=request.user)[:1]

		userorder = UserOrderTable()
		userorder.user = request.user
		userorder.status = 1
		userorder.price = all_prices
		if address:
			userorder.address = address[0]
		else:
			userorder.address_id = 1

		userorder.save()

		for oid in orderids:
			cart = UserCart.objects.get(id=int(oid))
			order = UserOrder()
			order.table = userorder
			order.product = cart.product
			order.count = cart.count

			cart.delete()

			order.save()
		return HttpResponse('{"msg":"正在生成订单"}', content_type='application/json')

class UserFavView(View):
	def post(self, request):
		pro_id = request.POST.get('pro_id', 0)

		product = Product.objects.get(id=int(pro_id))

		if not request.user.is_authenticated():
			# 判断用户是否登录、
			return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

		exist_records = UserFavorite.objects.filter(user=request.user, product=product)
		if exist_records:
			# 记录已存在，表示取消收藏
			exist_records.delete()
			'''
			course = Course.objects.get(id=int(fav_id))
			course.fav_nums -= 1
			if course.fav_nums < 0:
				course.fav_nums = 0
			course.save()
			'''

			return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
		else:
			user_fav = UserFavorite()
			user_fav.user = request.user
			user_fav.product = product
			user_fav.save()

			'''
			course = Course.objects.get(id=int(fav_id))
			course.fav_nums += 1
			'''

			return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

class AddCommentView(View):
	# 添加评论
	def post(self, request):
		if not request.user.is_authenticated():
			# 判断用户是否登录、
			return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

		course_id = request.POST.get('course_id', 0)
		comments = request.POST.get('comments', u'')
		if course_id > 0 and comments:
			course_comments = CourseComments()
			course = Course.objects.get(id=int(course_id))
			course_comments.course = course
			course_comments.comments = comments
			course_comments.user = request.user
			course_comments.save()
			return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')