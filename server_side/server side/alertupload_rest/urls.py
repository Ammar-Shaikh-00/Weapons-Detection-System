
from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as rest_framework_views
urlpatterns = [
    path('images/', views.post_alert, name='post_alert'),
    re_path(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

]