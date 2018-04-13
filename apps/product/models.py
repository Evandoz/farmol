# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

# Create your models here.

class Catalog(models.Model):
	name = models.CharField(max_length=100, verbose_name=u'目录名称')
	slug = models.SlugField(max_length=200, verbose_name=u'目录链接')
	desc = models.TextField(blank=True, verbose_name=u'目录描述')
	publisher = models.CharField(max_length=100, verbose_name='发布者')
	pub_date = models.DateTimeField(default=datetime.now, verbose_name=u'发布时间')

	class Meta:
		verbose_name = u'产品目录'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

class CatalogCategory(models.Model):
	catalog = models.ForeignKey(Catalog, related_name='categories', verbose_name=u'分类目录')
	parent = models.ForeignKey('self', blank=True, null=True, related_name='children', verbose_name=u'上级目录')
	name = models.CharField(max_length=100, verbose_name=u'目录名称')
	slug = models.SlugField(max_length=100, verbose_name=u'目录链接')
	desc = models.TextField(blank=True, verbose_name=u'目录描述')

	class Meta:
		verbose_name = u'产品管理'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		if self.parent:
			return '{0}:{1}-{2}'.format(self.catalog.name, self.parent.name, self.name)
		return '{0}:{1}'.format(self.catalog.name, self.name)

def product_directory_path(instance, filename):
	return 'product/catalog_{0}/{1}'.format(instance.category.id, filename)

class Product(models.Model):
	category = models.ForeignKey(CatalogCategory, related_name='products', verbose_name=u'目录')
	name = models.CharField(max_length=100, verbose_name=u'名称')
	slug = models.SlugField(max_length=100, verbose_name=u'链接')
	desc = models.TextField(verbose_name=u'描述')
	photo = models.ImageField(upload_to=product_directory_path, verbose_name=u'图片')
	manufacturer = models.CharField(max_length=300, blank=True, verbose_name=u'供应商')
	price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u'价格')

	class Meta:
		verbose_name = u'产品列表'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

class ProductAttribute(models.Model):
	name = models.CharField(max_length=100, verbose_name=u'属性名') # 属性名
	desc = models.TextField(blank=True, verbose_name=u'属性描述')

	class Meta:
		verbose_name = u'产品属性'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name

class ProductDetail(models.Model):
	product = models.ForeignKey(Product, related_name='details', verbose_name=u'产品')
	attribute = models.ForeignKey(ProductAttribute, verbose_name=u'属性名')
	value = models.CharField(max_length=150, verbose_name=u'属性值') # 属性值
	desc = models.TextField(blank=True, verbose_name=u'描述')

	class Meta:
		verbose_name = u'产品详情'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}:{1}-{2}'.format(self.product, self.attribute, self.value)