
from django.urls import path
from products.views import product_category_views as views


urlpatterns = [
	path('api/v1/product_category/all/', views.getAllProductCategory),

	path('api/v1/product_category/without_pagination/all/', views.getAllProductCategoryWithoutPagination),

	path('api/v1/product_category/<int:pk>', views.getAProductCategory),

	path('api/v1/product_category/search/', views.searchProductCategory),

	path('api/v1/product_category/create/', views.createProductCategory),

	path('api/v1/product_category/update/<int:pk>', views.updateProductCategory),

	path('api/v1/product_category/delete/<int:pk>', views.deleteProductCategory),



]