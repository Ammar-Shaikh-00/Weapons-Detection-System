from django.urls import path
from django.contrib.auth import views as auth_views # type: ignore
from . import views

urlpatterns = [
     path('login/', views.loginPage, name='login'),
     path('register/', views.registerPage, name='register'),
     path('logout/', views.logoutUser, name='logout'),
     path('', views.home, name='home'),
     path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
     path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
     path('reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
     path('reset_password_complete/',
         views.passwordResetComplete,
         name="password_reset_complete"),   
     path('alert/<uuid:pk>/', views.alert, name='alert'),
     path('<uuid:pk>.jpg', views.alert_image, name='alert_image'),
]