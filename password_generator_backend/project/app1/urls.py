from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.LoginLogout.as_view(),name='login'),
    path('password/generate/',views.PasswordGenerator.as_view(),name='password'),
    path('password/',views.PasswordList.as_view(),name='listpassword'),
    path('signin/',views.SignInNewUser.as_view(),name='signin'),
    
    
]
