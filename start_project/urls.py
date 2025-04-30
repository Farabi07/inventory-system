
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts
    path('user/', include('accounts.urls.user_urls')),
    path('role/', include('accounts.urls.role_urls'))
]
