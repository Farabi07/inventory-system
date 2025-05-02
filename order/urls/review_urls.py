from django.urls import path
from order.views import review_views as views


urlpatterns = [
    path('create/', views.createReview),
    path('product/<int:product_id>/', views.listProductReviews),
   

]