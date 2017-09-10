from django.shortcuts import render

from django.http import HttpResponse ,HttpResponseRedirect
from django.urls import reverse

from .models import *
from login.models import UserProfile


from quiz.models import Question
from django.core.files import File

# Create your views here.

def first_question():
    list = Question.objects.all()
    list = list[0]
    return list

def last_question():
    list = Question.objects.all()
    len_lst = len(list)
    list = list[len_lst-1]
    return list


def find_wrong_line(correct_file_list,user_file_list):
		#print correct_file_list
	if len(correct_file_list) > len(user_file_list):
		return -2
	for i in range(0,len(correct_file_list)):
		user_line = user_file_list[i].rstrip('\n')
		correct_line = correct_file_list[i].rstrip('\n')
		#print 'userline '+user_line
		#print 'correct_line '+correct_line
		if correct_line != user_line:
			# print correct_line+" expexted this "+ " but got "+user_line
			return i
	return -1

def calculate_wrong(request,question,code,wrong_line,correct_file_list,user_file_list):
	lines_per_testcase = code.lines_per_testcase
	lines_per_answer = code.lines_per_answer
	testcase_file = code.testcase_file
	
	#testcase number failed,+1 for 0-indexing
	ith_test_case_failed = (wrong_line/lines_per_answer)+1

	
	# file open
	testcase_file.open('r')
	testcase_file_list = testcase_file.readlines()
	testcase_file.close()
	# file close

	testcase_start = (lines_per_testcase*(ith_test_case_failed-1))+1
	testcase_end = testcase_start + lines_per_testcase
	
	failed_testcase = str()
	for x in testcase_file_list[testcase_start:testcase_end]:
		failed_testcase += x

	output_start = lines_per_answer*(ith_test_case_failed-1)
	output_end = output_start+lines_per_answer
	
	user_output = str()
	for x in user_file_list[output_start:output_end]:
		user_output +=x

	expected_output = str()
	for x in correct_file_list[output_start:output_end]:
		expected_output +=x 
	rmin = request.POST['min']
	rsec = request.POST['sec']
	submit  = UserSubmission.objects.create(User=request.user,question=question,failed_testcase=failed_testcase,expected_output=expected_output,user_output=user_output,ith_test_case_failed=ith_test_case_failed,rmin=rmin,rsec=rsec)	
	submit.save()


# will hit only on post
def answer_coding(request,pk,question):
	code = CodeQuestionExtend.objects.get(question=question)

	correct_file = code.answer_file	

	# file open
	correct_file.open(mode='r')
	correct_file_list = correct_file.readlines()
	correct_file.close()
	# file close

	user_file_list = request.FILES['userAnswer'].readlines()
	
	rmin = request.POST['min']
	rsec = request.POST['sec']

	wrong_line = find_wrong_line(correct_file_list,user_file_list)
	if wrong_line == -2:
		# dic['message'] = "some testcases are missing"
		submit = UserSubmission.objects.create(question=question,User=request.user,ith_test_case_failed=-2,rmin=rmin,rsec=rsec)
		submit.save()
	elif wrong_line != -1:
		calculate_wrong(request,question,code,wrong_line,correct_file_list,user_file_list)
	else:
		status = CodeUserStatus.objects.get(question=question,User=request.user)
		status.question_status = "Accepted"
		status.rmin = rmin
		status.save()
		submit  = UserSubmission.objects.create(User=request.user,question=question,ith_test_case_failed=-1,rmin=rmin,rsec=rsec)
		submit.save()
	return coding_display(request,pk,question)
	
def coding_display(request,pk,question):
	if request.method == 'GET':
		current_status = CodeUserStatus.objects.get(User=request.user,question=question)
		user = UserProfile.objects.get(user =request.user)
		code = CodeQuestionExtend.objects.get(question=question)
		testcase = CodeTestCase.objects.filter(question=question)
		user_submission  = UserSubmission.objects.filter(User=request.user,question=question).order_by('-pk')
		is_not_first_question = False
		islast_question = False
		if question != first_question():
			is_not_first_question = True
		if question == last_question():
			islast_question = True
		dic ={
		'question' : question,
		'code' :code,
		'testcase' : testcase,
		'current_status' : current_status,
		'last_question' : islast_question,
		'is_not_first_question' : is_not_first_question,
		'user' : user,
		'user_submission' : user_submission,
		}
		return render(request,'coding/index.html',dic)
	else:
		return HttpResponseRedirect(reverse('quiz:disp',args = (question.id,)))

def submission(request,pk,question):
	user_submission  = UserSubmission.objects.get(pk=pk,question=question)
	if user_submission.User == request.user:
		failed_testcase = str(user_submission.failed_testcase)
		failed_testcase = failed_testcase.strip("[']")
		failed_testcase = failed_testcase.split(',')
		print failed_testcase
		dic = {
		'ith_test_case_failed' : user_submission.ith_test_case_failed,
		'wrong_testcase' : failed_testcase,
		'expected_output' : user_submission.expected_output,
		'user_output' 	  : user_submission.user_output
		}
		return render(request,'coding/submission.html',dic)
		return HttpResponse("hi")
	else:
		return HttpResponse("You dont own this submission")
