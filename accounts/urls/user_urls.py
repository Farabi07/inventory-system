from accounts.views import user_views as views
from django.urls import path

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.login, name='login'),
    path('token/refresh/', views.token_refresh_view, name='token_refresh'),
    path('reset-password/', views.reset_password, name='reset_password'),
]