# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=8)

class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=8)
	captcha = CaptchaField( error_messages={'invalid': u'验证码错误'})

class ForgetForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})

class ResetForm(forms.Form):
	password = forms.CharField(required=True, min_length=8)
	password2 = forms.CharField(required=True, min_length=8)

class UploadImageForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['image']

class UploadInfoForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['nick_name', 'gender', 'address', 'mobile']