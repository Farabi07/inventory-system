from accounts.models import *
from django_filters import rest_framework as filters


class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name', ]


class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['name', ]


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', ]


class LoginHistoryFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="user__username", lookup_expr='icontains')

    class Meta:
        model = LoginHistory
        fields = ['username', ]



