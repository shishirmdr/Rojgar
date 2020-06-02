from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('create', views.seller_create_view , name='create'),
    path('detail',views.seller_detail_view, name="detail"),
]


