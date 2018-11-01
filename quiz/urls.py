from django.conf.urls import url

from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^(?P<test_id>[0-9]+)/(?P<pk>[0-9]+)/disp/$',views.disp, name='display-question'),
    url(r'^(?P<test_id>[0-9]+)/create-status/',views.create_status, name = 'create-status'),
    url(r'^(?P<test_id>[0-9]+)/timer$',views.timer),
    url(r'^(?P<test_id>[0-9]+)/rules$',views.rules),
    url(r'^(?P<test_id>[0-9]+)/endtest$',views.endtest,name = 'end_test'),
]
