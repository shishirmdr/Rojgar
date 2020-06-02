from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup, name='signup'),
    path('results/', views.results, name='results'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name="logout"),

    # password retrieval
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_password_done.html"),
         name="password_reset_complete")

]
