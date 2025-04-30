from accounts.views import user_views as views
from django.urls import path

urlpatterns = [
    path('signup/', views.register),
    path('login/', views.login),
    path('token/refresh/', views.token_refresh_view),
    path('reset-password/', views.reset_password),
    path('api/v1/user/without_pagination/all/', views.getAllUserWithoutPagination),
    path('api/v1/user/<int:pk>', views.getAUser),
    path('api/v1/user/search/', views.searchUser),
    path('api/v1/user/update/<int:pk>', views.updateUser),
    path('api/v1/user/delete/<int:pk>', views.deleteUser),
]