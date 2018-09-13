"""email_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include,url
from django.views.generic import TemplateView

from email_wrapper.views import login_view, after_login_view, mail_deliver_view, UserFormView, UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',login_view, name='login'),
    #path('send/',after_login_view, name='send_mail'),
    path('send/',mail_deliver_view, name='send_mail'),
    #path('send/',ses_deliver_view, name='send_mail'),
    #url('accounts/',include('accounts.urls')),
    #path('register/',UserFormView,name='register_me'),
    path('register/',UserFormView.as_view(),name='register_me'),
    path('',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    #url(r'^register$', 'UserFormView', name='register_me'),
]
