from django.urls import path
from . import views


urlpatterns = [
    path('login',views.LoginLogout.as_view(),name='loginview'),
    path('logout',views.LoginLogout.as_view(),name='logoutview'),
    
]
