from django.conf.urls import url

from .views import UserFavView, ShowOrderView, GenerateOrderView, DeleteCartView, UpdateCartView, AddCartView, DetailView, ShopView

urlpatterns = [
	url(r'^list/$', ShopView.as_view(), name='list'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
    url(r'^addcart/$', AddCartView.as_view(), name='addcart'),
    url(r'^updatecart/$', UpdateCartView.as_view(), name='updatecart'),
    url(r'^deletecart/$', DeleteCartView.as_view(), name='deletecart'),
    url(r'^generateorder/$', GenerateOrderView.as_view(), name='generateorder'),
    url(r'^showorder/$', ShowOrderView.as_view(), name='showorder'),
    url(r'^fav/$', UserFavView.as_view(), name='fav'),
]
