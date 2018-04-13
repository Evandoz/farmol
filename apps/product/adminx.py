# -*- coding: utf-8 -*-

import xadmin

from .models import ProductDetail, ProductAttribute, Product, CatalogCategory, Catalog

class CatalogAdmin(object):
	list_display = ['name', 'desc', 'publisher', 'pub_date']
	search_fields = ['name', 'desc', 'publisher']
	list_filter = ['name', 'desc', 'publisher', 'pub_date']
	#model_icon = 'fa fa-user'

class CatalogCategoryAdmin(object):
	list_display = ['__unicode__', 'desc', 'parent']
	search_fields = ['desc', 'parent'] # '__unicode__',
	list_filter = ['desc', 'parent'] # '__unicode__',
	#model_icon = 'fa fa-user'

class ProductAdmin(object):
	list_display = ['name', 'desc', 'category']
	search_fields = ['name', 'desc', 'category']
	list_filter = ['name', 'desc', 'category']
	#model_icon = 'fa fa-user'

class ProductAttributeAdmin(object):
	list_display = ['name', 'desc']
	search_fields = ['name', 'desc']
	list_filter = ['name', 'desc']
	#model_icon = 'fa fa-user'

class ProductDetailAdmin(object):
	list_display = ['product', 'attribute', 'desc']
	search_fields = ['product', 'attribute', 'desc']
	list_filter = ['product', 'attribute', 'desc']
	#model_icon = 'fa fa-user'

xadmin.site.register(Catalog, CatalogAdmin)
xadmin.site.register(CatalogCategory, CatalogCategoryAdmin)
xadmin.site.register(Product, ProductAdmin)
xadmin.site.register(ProductAttribute, ProductAttributeAdmin)
xadmin.site.register(ProductDetail, ProductDetailAdmin)