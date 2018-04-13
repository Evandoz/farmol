from django.conf.urls import url

from .views import UserCenterFavView, UserMessageView, UserOrderView, UserCartView, UserInfoView, UserEmailView, UserEmailCodeView, UserPwdView, UserImageView, UserInfoView

urlpatterns = [
	url(r'^info/$', UserInfoView.as_view(), name='info'),
	url(r'^image/$', UserImageView.as_view(), name='image'),
	url(r'^pwd/$', UserPwdView.as_view(), name='pwd'),
	url(r'^code/$', UserEmailCodeView.as_view(), name='code'),
	url(r'^email/$', UserEmailView.as_view(), name='email'),
	url(r'^info/$', UserInfoView.as_view(), name='info'),
	url(r'^cart/$', UserCartView.as_view(), name='cart'),
	url(r'^order/$', UserOrderView.as_view(), name='order'),
	url(r'^message/$', UserMessageView.as_view(), name='message'),
	url(r'^fav/$', UserCenterFavView.as_view(), name='fav'),
]
