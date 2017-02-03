from django.conf.urls import  url
from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$',views.ans, name='ans'),
    url(r'^(?P<pk>[0-9]+)/disp/$',views.disp, name='disp'),
    url(r'^pop/$',views.s_pop, name = 'pop'),
    #not used
    url(r'^(?P<pk>[0-9]+)/nq/$',views.nth_question, name='nq'),   
]