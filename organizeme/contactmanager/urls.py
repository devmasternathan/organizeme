from django.conf.urls import url
from . import views

app_name = "organizeme"

urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^manager/$', views.manager_view, name='manager'),
    url(r'^demo/$', views.demo_view, name='demo'),
    url(r'^logout/$', views.logout_view, name='logout')
]
