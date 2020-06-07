from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search-results'),

    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', views.TagDetailsView.as_view(),
         name='tag-details'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('public/<int:pk>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('public/<int:pk>/<str:action>/', views.UserActionView.as_view(), name='user-action'),
]
