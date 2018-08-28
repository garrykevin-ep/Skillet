from django.shortcuts import render
from django.http import HttpResponse
from .models import nav_drop_down,card
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from quiz.views import first_question
from quiz.models import TestStatus , Test
from django.db import IntegrityError
# from .config import *

# Create your views here.
@login_required(login_url = '/')
def dashboard(request):
	tests = Test.objects.filter(publish=True)
	for test in tests:
		try:
			TestStatus.objects.create(user=request.user,test=test,minute=test.minute,second=test.second)
		except IntegrityError:
			pass
	test_statuses = TestStatus.objects.filter(user = request.user,completed = False,test__publish=True)	
	return render(request,'dashboard/index.html',{"test_statuses" : test_statuses})