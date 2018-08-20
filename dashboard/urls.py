from django.conf.urls import url
# from .views import 
from . import views

app_name = 'dash'

urlpatterns = [
    url(r'^',views.dashboard,name="board"),
]