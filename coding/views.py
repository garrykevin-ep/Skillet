from django.shortcuts import render

from django.http import HttpResponse

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



# will hit only on post
def answer_coding(request,pk,question):
	code = CodeQuestionExtend.objects.get(question=question)
	testcase = CodeTestCase.objects.filter(question=question)
	#user_submission = UserSubmission.objects.create(User=request.user,question=question,user_output=request.FILES['userAnswer'])
	#user_submission.save()

	dic = {}
	dic['code'] = code
	dic['testcase']  = testcase

	# print testcase

	correct_file = code.answer_file

	# file open
	correct_file.open(mode='r')
	correct_file_list = correct_file.readlines()
	correct_file.close()
	# file close

	user_file_list = request.FILES['userAnswer'].readlines()
	
	wrong_line = find_wrong_line(correct_file_list,user_file_list)
	if wrong_line == -2:
		dic['message'] = "some testcases are missing"
	elif wrong_line != -1:
		lines_per_testcase = code.lines_per_testcase
		lines_per_answer = code.lines_per_answer
		testcase_file = code.testcase_file
		
		#testcase number failed,+1 for 0-indexing
		ith_test_case_failed = (wrong_line/lines_per_answer)+1
		dic['testcase_failed'] = ith_test_case_failed
		
		# file open
		testcase_file.open('r')
		testcase_file_list = testcase_file.readlines()
		testcase_file.close()
		# file close

		testcase_start = (lines_per_testcase*(ith_test_case_failed-1))+1
		testcase_end = testcase_start + lines_per_testcase
		
		
		dic['wrong_testcase'] = testcase_file_list[testcase_start:testcase_end]

		output_start = lines_per_answer*(ith_test_case_failed-1)
		output_end = output_start+lines_per_answer
		

		dic['user_output'] = user_file_list[output_start:output_end]
		dic['expected_output'] = correct_file_list[output_start:output_end]
		dic['message'] = "wrong answer"
	else:
		dic['message'] = "correct answer"
	return coding_display(request,pk,question,dic)
	
def coding_display(request,pk,question,dic):
	current_status = CodeUserStatus.objects.get(User=request.user,question=question)
	user = UserProfile.objects.get(user =request.user)
	if question != first_question():
		is_not_first_question = True
	if question == last_question():
		islast_question = True
	if request.method == 'POST':
		dic['question'] = question
		dic['current_status'] = current_status
		dic['last_question'] = islast_question
		dic['is_not_first_question'] = is_not_first_question
		dic['user'] = user
		return render(request,'coding/index.html',dic)
	else:
		code = CodeQuestionExtend.objects.get(question=question)
		testcase = CodeTestCase.objects.filter(question=question)
		dic ={
		'question' : question,
		'code' :code,
		'testcase' : testcase,
		'current_status' : current_status,
		'last_question' : islast_question,
		'is_not_first_question' : is_not_first_question,
		'user' : user
		}
		return render(request,'coding/index.html',dic)
