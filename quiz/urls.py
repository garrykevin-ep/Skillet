from django.conf.urls import  url
from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$',views.index,name = 'index'),
    url(r'^(?P<pk>[0-9]+)/ans/$',views.ans, name='ans')
]