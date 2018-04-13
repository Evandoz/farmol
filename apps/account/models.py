# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser

from datetime import datetime

from django.db import models

# Create your models here.

class UserProfile(AbstractUser):
	nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
	gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default=u'female', verbose_name=u'性别')
	address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
	mobile = models.CharField(max_length=11, null=True, verbose_name=u'手机号', blank=True)
	image = models.ImageField(upload_to=u'avatar/%Y/%m', verbose_name=u'图像', default=u'avatar/default.png', max_length=100)

	class Meta:
		verbose_name = u'用户信息'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.username

class EmailVerifyRecord(models.Model):
	code = models.CharField(max_length=20, verbose_name=u'验证码')
	email = models.EmailField(max_length=50, verbose_name=u'邮箱')
	send_type = models.CharField(max_length=8, verbose_name=u'验证码类型', choices=(('register', u'注册'), ('forget', u'找回密码'), ('update', u'修改邮箱')))
	send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

	class Meta:
		verbose_name=u'邮箱验证码'
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return '{0}({1})'.format(self.code, self.email)