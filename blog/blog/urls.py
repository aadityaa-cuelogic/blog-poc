"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# Add this import
from django.contrib.auth import views as auth_views
from blogs import views
from blogs.forms import LoginForm, RegistrationForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blogs.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html',
        'authentication_form': LoginForm}, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'forgot_password.html'}, name="forgot_password"),
    url(r'^password_reset/done$', auth_views.password_reset_done,{
        'template_name':'forgot_password_done.html'}, name='password_reset_done'),

    url(r'^password_change/$', auth_views.password_change,
        {'template_name':'password_change.html'}, name="password_change"),
    url(r'^password_change/done$', auth_views.password_change_done,
        {'template_name': 'password_change_done.html'}, name='password_change_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name="password_reset_complete"),

    url(r'^register/$', views.register, name="register"),
    url(r'^register/success/$', views.register_success,),
]
