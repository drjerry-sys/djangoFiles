"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from docutils.nodes import author
from django.views.generic import TemplateView
from instagram.accountapp import views as account_view
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_view.homePage, name='homepage'),
    path('search/', account_view.search, name='search'),
    path('accounts/edit/', account_view.editProfile, {'val': '1'}, name='accnt'),
    path('user/register/confirm', account_view.userRegConfirm, name='confirm_reg'),
    path('user/register/', account_view.userRegister, name='register'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('password_reset/', account_view.toReset, name='password_reset'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change/password/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('edit/done', account_view.editProfile, {'val': '2'}, name='edit_done'),
    path('edit/login_activity', account_view.editProfile, {'val': '3'}, name='act_login'),
    path('api/', include('instagram.api.urls')),
    path('<str:username>/', account_view.myProfile, name='profile_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)