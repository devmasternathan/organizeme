from django.conf.urls import url
from . import views

app_name = "organizeme"

urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^manager/(?P<slug>[-\w]+)/$', views.ContactFormView.as_view(), name='manager'),
    url(r'^demo/(?P<slug>[-\w]+)/$', views.ContactFormView.as_view(), name='demo'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.EditFormView.as_view(), name='edit'),
    url(r'^remove/(?P<id>[-\w]+)/$', views.remove_view, name='remove')
]
