# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from account.models import UserProfile
from product.models import Product

# Create your models here.


class UserCart(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u'用户')
	product = models.ForeignKey(Product, verbose_name=u'商品')
	count = models.IntegerField(default=0, verbose_name=u'数量')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

	class Meta:
		verbose_name = u'购物车'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.user, self.product)

class UserAddress(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u'用户')
	address = models.CharField(max_length=500,verbose_name=u'收货地址')
	mobile = models.CharField(max_length=11, verbose_name=u'手机号')
	person = models.CharField(max_length=100, verbose_name=u'收货人')

	class Meta:
		verbose_name = u'收货地址'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return unicode(self.user)

class UserOrderTable(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u'用户')
	status = models.IntegerField(choices=(('1', u'未付款'), ('2', u'已付款'), ('3', u'待发货'), ('4', u'已发货'), ('5', u'已完成')), default=1, verbose_name=u'订单状态')
	price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u'金额')
	address = models.ForeignKey(UserAddress, verbose_name=u'收货地址')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

	class Meta:
		verbose_name = u'用户订单'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return unicode(self.user)

class UserOrder(models.Model):
	table = models.ForeignKey(UserOrderTable, verbose_name=u'订单')
	product = models.ForeignKey(Product, verbose_name=u'商品')
	count = models.IntegerField(default=0, verbose_name=u'数量')

	class Meta:
		verbose_name = u'订单'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.table, self.product)

class UserComment(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u'用户')
	product = models.ForeignKey(Product, verbose_name=u'商品')
	comment = models.CharField(max_length=200, verbose_name=u'评论')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'评论时间')

	class Meta:
		verbose_name = u'用户评论'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.user, self.product)

class UserFavorite(models.Model):
	user = models.ForeignKey(UserProfile, verbose_name=u'用户')
	product = models.ForeignKey(Product, verbose_name=u'商品')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

	class Meta:
		verbose_name = u'用户收藏'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.user, self.product)

class UserMessage(models.Model):
	user = models.IntegerField(default=0,verbose_name=u'接收用户')
	message = models.CharField(max_length=500, verbose_name=u'消息内容')
	has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'消息时间')

	class Meta:
		verbose_name = u'用户消息'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}-{1}'.format(self.user, self.message)