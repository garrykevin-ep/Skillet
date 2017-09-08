from django.conf.urls import url

from . import views

app_name = 'code'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/(?P<question>[0-9]+)/$',views.submission, name='submission'),
]
