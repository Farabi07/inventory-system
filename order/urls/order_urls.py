from django.urls import path
from order.views import order_views as views


urlpatterns = [
    path('api/order/create/', views.createOrder),
    path('api/order/all/', views.getAllOrders),
    path('api/order/<int:pk>/', views.getAnOrder),
    path('api/order/search/', views.searchOrders),
    path('api/order/update/<int:pk>/', views.updateOrder),
    path('api/order/delete/<int:pk>/', views.deleteOrder),
    path('api/sales-invoice/<int:order_id>/', views.getSalesInvoice),
    path('api/sales-history/', views.getSalesHistory)
   

]