
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts
    path('user/', include('accounts.urls.user_urls')),
    path('role/', include('accounts.urls.role_urls')),
    # products
    path('product/',include('products.urls.product_urls')),
    path('product_category/',include('products.urls.product_category_urls')),
    # order
    path('orders/', include('order.urls.order_urls')),
    path('review/', include('order.urls.review_urls')),

    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
	re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
