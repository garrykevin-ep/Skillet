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
	test = TestStatus.objects.filter(user = request.user)
	print (test)
	url_instance = []
	for test_obj in test:
		first_ques = first_question(test_obj.test)
		url = "/"+str(test_obj.test.id)+"/"+str(first_ques.id)+"/disp"
		url_instance.append(url)
	test_list = zip(test,url_instance)
	context = {
		"test" : test_list ,
	}
	return render(request,'dashboard/index.html',context)