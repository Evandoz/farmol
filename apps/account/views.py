# -*- coding: utf-8 -*-
import json
from django.shortcuts import render_to_response, render
from django.views.generic.base import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

import datetime



from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import EmailVerifyRecord, UserProfile
from .forms import UploadInfoForm, UploadImageForm, ResetForm, ForgetForm, RegisterForm, LoginForm

from operation.models import UserFavorite, UserMessage, UserOrder, UserOrderTable, UserCart

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin

# Create your views here.

class CustomBackend(ModelBackend):
	def authenticate(self, username = None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None

class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')

	def  post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('index'))
					#return render(request, 'index.html')
				else:
					return render(request, 'login.html', {'msg': '用户未激活'})
			else:
				return render(request, 'login.html', {'msg': '用户名或密码错误'})
		else:
			return render(request, 'login.html', {'login_form': login_form})

class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(reverse('index'))

class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get('email', '')
			pass_word = request.POST.get('password', '')
			if UserProfile.objects.filter(email=user_name):
				return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.is_active = False
			user_profile.password = make_password(pass_word)
			user_profile.save()

			# 系统发送消息
			user_message = UserMessage()
			user_message.user = user_profile.id
			user_message.message = u'欢迎注册'
			user_message.save()

			send_register_email(user_name, 'register')
			return render(request, 'login.html')
		else:
			return render(request, 'register.html', {'register_form': register_form})

class ActiveUserView(View):
	def get(self, request, pk):
		all_records = EmailVerifyRecord.objects.filter(code=pk)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
		else:
			return HttpResponse('{"status":"fail"}', content_type='application/json')
		return render(request, 'login.html')

class ForgetPwdView(View):
	def get(self, request):
		forget_form = ForgetForm()
		return render(request, 'forgetpwd.html', {'forget_form': forget_form})

	def post(self, request):
		forget_form = ForgetForm(request.POST)
		if forget_form.is_valid():
			email = request.POST.get('email', '')
			send_register_email(email, 'forget')
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
	def get(self, request, pk):
		all_records = EmailVerifyRecord.objects.filter(code=pk)
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, 'resetpwd.html', {'email': email})
		return render(request, 'login.html')

class ModifyView(View):
	def post(self, request):

		reset_form = ResetForm(request.POST)
		if reset_form.is_valid():
			pwd = request.POST.get('password', '')
			pwd2 = request.POST.get('password2', '')
			email = request.POST.get('email', '')
			if pwd != pwd2:
				return render(request, 'resetpwd.html', {'email': email, 'msg': '密码不一致'})
			user = UserProfile.objects.get(email=email)
			user.password = make_password(pwd2)
			user.save()
			return render(request, 'login.html')
		else:
			email = request.POST.get('email', '')
			return render(request, 'resetpwd.html', {'email': email, 'reset_form': reset_form})

class UserInfoView(LoginRequireMixin, View):
	def get(self, request):

		carts = UserCart.objects.filter(user=request.user)
		carts_nums = carts.count()

		all_price = 0
		for cart in carts:
			all_price += cart.product.price * cart.count

		carts = carts[:3]

		return render(request, 'user-info.html', {
		    'carts': carts,
		    'carts_nums': carts_nums,
		    "all_price": all_price
		})

	def post(self, request):
		userinfo_form = UploadInfoForm(request.POST, instance=request.user)

		if userinfo_form.is_valid():
			userinfo_form.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')

class UserImageView(LoginRequireMixin, View):
	def post(self, request):
		image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)

		if image_form.is_valid():
			image = image_form.cleaned_data['image']
			image_form.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail"}', content_type='application/json')

class UserPwdView(LoginRequireMixin, View):
	# 个人中心修改密码
	def post(self, request):
		reset_form = ResetForm(request.POST)
		if reset_form.is_valid():
			pwd = request.POST.get('password', '')
			pwd2 = request.POST.get('password2', '')
			if pwd != pwd2:
				return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
			user = request.user
			user.password = make_password(pwd2)
			user.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')

class UserEmailCodeView(LoginRequireMixin, View):
	# 发送邮箱验证码
	def get(self, request):
		email = request.GET.get('email', '')

		if UserProfile.objects.filter(email=email):
			return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')

		send_register_email(email, 'update')
		return HttpResponse('{"status":"success"}', content_type='application/json')

class UserEmailView(LoginRequireMixin, View):
	# 修改个人邮箱
	def post(self, request):
		email = request.POST.get('email', '')
		code = request.POST.get('code', '')

		exist_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
		if exist_record:
			user = request.user
			user.email = email
			user.save()
			return HttpResponse('{"status":"success"}', content_type='application/json')
		else:
			return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class UserCartView(LoginRequireMixin, View):
	def get(self, request):

		all_carts = UserCart.objects.filter(user=request.user)
		carts = all_carts[:3]
		carts_nums = all_carts.count()

		all_price = 0
		for cart in all_carts:
			all_price += cart.product.price * cart.count


		return render(request, 'cart.html', {
		    "all_carts": all_carts,
		    "carts": carts,
		    "carts_nums": carts_nums,
		    "all_price": all_price
		})

class UserOrderView(LoginRequireMixin, View):
	def get(self, request):
		all_orders = UserOrderTable.objects.filter(user=request.user).order_by('-add_time')
		orders_nums = all_orders.count()

		y = request.GET.get('year_from', 2017)
		m = request.GET.get('month_from', 6)
		d = request.GET.get('day_from', 1)
		date_from = datetime.datetime(int(y), int(m), int(d), 0, 0)
		y = request.GET.get('year_to', 2017)
		m = request.GET.get('month_to', 6)
		d = request.GET.get('day_to', 3)
		date_to = datetime.datetime(int(y), int(m), int(d), 0, 0)

		if date_from and date_to:
			all_orders = UserOrderTable.objects.filter(add_time__range=(date_from, date_to))

		sort = request.GET.get('sort', '')

		if sort:
			if sort == 'date':
				all_orders = all_orders.order_by('add_time')
			if sort == 'price':
				all_orders = all_orders.order_by('-price')

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_orders, 6, request=request)
		orders = p.page(page)

		return render(request, 'order-history.html', {
		    "all_orders": orders
		})


class UserMessageView(LoginRequireMixin, View):
	def get(self, request):
		all_messages = UserMessage.objects.filter(user=request.user.id)

		all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
		for unread_message in all_unread_messages:
			unread_message.has_read = True
			unread_message.save()

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(all_messages, 3, request=request)
		messages = p.page(page)

		return render(request, 'newsletter.html',{
		    'all_messages': messages
		})

class UserCenterFavView(LoginRequireMixin, View):
	def get(self, request):

		fav_products = UserFavorite.objects.filter(user=request.user)

		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		p = Paginator(fav_products, 3, request=request)
		products = p.page(page)

		return render(request, 'fav.html',{
		    'fav_products': products
		})