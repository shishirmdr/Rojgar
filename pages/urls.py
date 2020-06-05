from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailsView.as_view(),
         name='category-details'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('public/<int:pk>/', views.PublicProfileView.as_view(),
         name='public_profile')
]
