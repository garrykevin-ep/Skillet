from django.conf.urls import url

from . import views

app_name = 'login'

urlpatterns = [
	url(r'^$',views.auth_login,name = 'login'),
    url(r'^auth/$',views.auth,name = 'auth'),
    url(r'^register/$',views.register,name = 'register'),
    url(r'^logout/$',views.logout_view, name = 'logout'),
]
