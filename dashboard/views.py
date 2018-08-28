from django.shortcuts import render
from django.http import HttpResponse
from .models import nav_drop_down,card
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from quiz.views import first_question
from quiz.models import TestStatus , Test
# from .config import *

# Create your views here.
@login_required(login_url = '/')
def dashboard(request):
	test_statuses = TestStatus.objects.filter(user = request.user,completed = False)	
	return render(request,'dashboard/index.html',{"test_statuses" : test_statuses})