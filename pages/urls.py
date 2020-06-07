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

    path('public/<int:pk>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('public/<int:pk>/<str:action>/', views.UserActionView.as_view(), name='user-action'),

    path('public/comment/<int:pk>/', views.CommentView.as_view(), name='comment'),

    path('favourite_profile/<int:pk>/', views.favourite_profile, name="favourite_profile"),
    path('favourites/', views.profile_favourite_list, name="profile_favourite_list")
]
