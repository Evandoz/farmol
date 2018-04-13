# -*- coding: utf-8 -*-
import xadmin

from .models import UserMessage, UserFavorite, UserComment, UserCart

class UserCartAdmin(object):
	list_display = ['user', 'product', 'count', 'add_time']
	search_fields = ['user', 'product', 'count']
	list_filter = ['user', 'product', 'count', 'add_time']

class UserCommentAdmin(object):
	list_display = ['user', 'product', 'comment', 'add_time']
	search_fields = ['user', 'product', 'comment']
	list_filter = ['user', 'product', 'comment', 'add_time']
	model_icon = 'fa fa-comments'

class UserFavoriteAdmin(object):
	list_display = ['user', 'product', 'add_time']
	search_fields = ['user', 'product']
	list_filter = ['user', 'product', 'add_time']

class UserMessageAdmin(object):
	list_display = ['user', 'message', 'has_read', 'add_time']
	search_fields = ['user', 'message', 'has_read']
	list_filter = ['user', 'message', 'has_read', 'add_time']

xadmin.site.register(UserCart, UserCartAdmin)
xadmin.site.register(UserComment, UserCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)