"""benie_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path as url, include
from benie_app import views, views_auth
from knox import views as knox_views

urlpatterns = [
    path('password/change/<int:pk>',views_auth.ChangePasswordView.as_view(),name='change-password'),
    url(r'^password/reset/request/$',views_auth.PasswordResetRequest.as_view(),name='reset-password-request'),
    path('password/reset/confirmed/<int:pk>',views_auth.ResetPasswordView.as_view(),name='reset-password-confirmed'),
    path('password/reset/complete/<slug:uidb64>/<slug:token>/',views_auth.activate,name='reset-password-complete'),
    url(r'^auth/', include('knox.urls')),
    url(r'^auth/register$', views_auth.RegisterView.as_view(),name="register"),
    url(r'^auth/login$', views_auth.LoginView.as_view(),name="login"),
    url(r'^auth/logout/$', knox_views.LogoutView.as_view(),name="knox-logout"),
    url(r'^user/$', views_auth.UserView.as_view(),name="user"),
    path('user/update/<int:pk>', views_auth.UpdateUserView.as_view(),name="update-user"),
    url(r'^all-users/$',views_auth.UserProfiles.as_view(),name="all-users"),
    url(r'^all/admins/$',views_auth.AllAdmins.as_view(),name='all-admins'),
]

