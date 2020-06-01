from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('results/', views.results, name='results'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name="logout"),
]