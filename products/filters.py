from products.models import *
from django_filters import rest_framework as filters





class ProductCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = ProductCategory
        fields = ['name', ]

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name',]
