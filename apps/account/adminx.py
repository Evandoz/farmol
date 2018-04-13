# -*- coding: utf-8 -*-

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from django.contrib.auth.models import User

from .models import EmailVerifyRecord, UserProfile

class BaseSettings(object):
	enable_themes = True
	use_bootswatch = True

class GlobalSettings(object):
	site_title = "Farm Manager"
	site_footer = "Farm Online"
	menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']
	model_icon = 'fa fa-user'

xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)