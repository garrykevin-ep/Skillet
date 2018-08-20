from difflib import SequenceMatcher

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.urls import reverse

from login.models import UserProfile

from .models import *

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# navigation helper functions
def no_of_Question(): 
    #not used
    return Question.objects.all().count()

def first_question(test_id):
    return Question.objects.filter(test=test_id).first()

def last_question(test_id):
    return Question.objects.filter(test=test_id).last()    

def next_question(pk,test_id):
    pk = int(pk)
    if pk != last_question(test_id).id:
        return  Question.objects.filter(test= test_id,id__gt = pk).first()
    else:
        return None

def prev_question(pk,test_id):
    pk = int(pk)
    if pk != first_question(test_id).id:
        return Question.objects.filter(test= test_id,id__lt = pk).last()
    else:
        return None

def nth_question(pk,test_id):
    questions = Question.objects.filter(test=test_id)
    pk = int(pk)
    pk = pk -1
    return questions[pk]

#question helper functions
def add_mark(test_status):
    test_status.mark += 1
    test_status.save()

def dec_mark(test_status):
    test_status.mark -= 1 
    test_status.save()

def save_time(request,test_status):
    #test_status is teststatus object
    print (request.POST['sec'])
    if test_status.minute >= int(request.POST['min']):
        test_status.minute = int(request.POST['min'])
        test_status.second = int(request.POST['sec'])
        test_status.save()

# get correct ans
def get_ans_multi(question):
    return MultiChoice.objects.get(question=question,answer='Yes')
    
def get_current_status(question,current_user):
    if question.type == 'mcq':
        return MultiStatus.objects.get(User= current_user,question = question)
    elif question.type == 'fill':
        return FillStatus.objects.get(User= current_user,question = question)

def get_choices(question):
    if question.type == 'mcq':
        return MultiChoice.objects.filter(question=question,question__test=question.test)
    elif question.type == 'fill':
        return FillChoice.objects.filter(question=question,test=question.test)
#####TO BE done
def get_all_status(current_user,test_id):
    mcq_list = MultiStatus.objects.filter(question__test=test_id, User=current_user)
    fill_list  = FillStatus.objects.filter(question__test=test_id, User=current_user)
    full = list(mcq_list)+list(fill_list)
    full =  sorted(full,key=lambda x: x.question.id)
    return full

def is_fill_correct(question,currentAnswer):
    #checks similar if matches > .5 correct
    options = get_choices(question)
    for option in options:
        if similar(currentAnswer,option.choice_text) > .5:
            return  True
    return False

def disp_next_question(question,pk,test_id):
    next_Question = next_question(pk,test_id)
    if(next_Question != None):
            return HttpResponseRedirect(reverse('quiz:display-question',args = (test_id,next_Question.id,)))
    else:
        return redirect('login:logout')
        #TODO landing page
        #return HttpResponse("Thank You") #need to check how many left unanswerd

    
# main functions , post hits here
@login_required(login_url = '/')
def create_status(request,test_id):
    current_user = request.user
    test = get_object_or_404(Test,pk=test_id)
    try:
        TestStatus.objects.create(user=current_user,test=test,minute=test.minute,second=test.second,mark=0)
    except IntegrityError:
        pass
    questions = Question.objects.filter(test=test_id)
    for question in questions:
        if question.type == 'mcq':
           MultiStatus.objects.get_or_create(User = current_user,question = question)
        elif question.type == 'fill':
           FillStatus.objects.get_or_create(User = current_user,question= question)
    return HttpResponseRedirect(reverse('quiz:display-question',args = (test_id,first_question(test_id).id,)))


@login_required(login_url = '/')
def disp(request,test_id,pk):
    question = get_object_or_404(Question,pk=pk)
    current_user = request.user
    if request.method == 'POST':
        nav = request.POST['nav']
        ans(request,test_id,pk)
        if nav  == 'Next' or nav == 'Finish':
            #function is just to check last question
            return disp_next_question(question,pk,test_id)
        elif nav == 'Previous':
            prev_q = prev_question(pk,test_id)
            return HttpResponseRedirect(reverse('quiz:display-question',args = (test_id,prev_q.id,)))
        else:
            nth_q = nth_question(nav,test_id)
            return HttpResponseRedirect(reverse('quiz:display-question',args = (test_id,nth_q.id,)))
    else:
        return display_question(request,pk,current_user,question,test_id)

@login_required(login_url = '/')
#actually ans post always
def ans(request,test_id,pk):
    current_user = request.user
    question = get_object_or_404(Question,pk=pk)
    status = get_current_status(question,current_user)
    test_status = TestStatus.objects.get(user=current_user,test=test_id)
    # user = UserProfile.objects.get(user = current_user.id)
    status.Qstatus = request.POST['status']
    status.save()
    save_time(request,test_status)
    if question.type == 'mcq':
        answer_multi(request,question,test_status,status)
    elif question.type == 'fill':
        answer_fill(request,test_status,question,status)

def answer_fill(request,test_status,question,status):
    currentAnswer = request.POST['answer']
    # fill is blank
    if currentAnswer == '':
        #last ans is correct
        if status.preResult != -1:  
            dec_mark(test_status)
        status.preResult = -1
        status.save()
    else:
        # fill not blank,ans is correct
        if is_fill_correct(question,currentAnswer):
            #two times correct answer
            if status.preResult != 1:
                add_mark(test_status)
                status.preResult = 1
                status.save()
        else:
            if status.preResult == 1:
                #not first time answering the question
                #wrong answer after correct ans
                dec_mark(test_status)
                status.preResult = 0
                status.save()
    status.answer = currentAnswer
    status.save()


def answer_multi(request,question,test_status,status):
    try:
        value = request.POST['choice']
        selected_choice = MultiChoice.objects.get(pk=value)
    except:
        # last ans is correct , no choice selected now
        if status.selected == get_ans_multi(question):
            dec_mark(test_status)
        status.selected = -1
        status.save()   
    else: 
        #ans is correct , choice is selected
        if(selected_choice.answer == 'Yes' ):
            #two times same correct answer
            if selected_choice.id != status.selected:
                add_mark(test_status)
        else:
            if status.selected != -1:
                #not first time answering the question
                pre_choice = MultiChoice.objects.get(pk = status.selected)
                if pre_choice.answer == 'Yes':
                    #wrong ans afer corect ans
                    dec_mark(test_status)
        #ans first time
        status.selected = value
        status.save()



def display_question(request,pk,current_user,question,test_id):
    if question.type == 'mcq' or question.type == 'fill':
        return multi_fill_display(request,pk,current_user,question,test_id)

def multi_fill_display(request,pk,current_user,question,test_id):
    #get request
    #can display multi choice or fillups
    pre_question = prev_question(pk,test_id)
    current_status = get_current_status(question,current_user)
    user = UserProfile.objects.get(user = current_user.id) 
    # print(first_question)
    dic ={
    'test_id' : int(test_id),
    'question' : question,
    'first_question': first_question(test_id),
    'last_question' : last_question(test_id),
    'pre_question' : pre_question,
    'next_question': next_question,
    #status for displaying status of other questions
    'status'  : get_all_status(current_user,test_id),
    'choice' : get_choices(question),
    'test_status' : TestStatus.objects.get(user=current_user,test=test_id),
    'current_status' : current_status, 
    'user' : user,
   }
    return render(request,'quiz/index.html',dic)



def timer(request,test_id):
    if request.method == 'POST':
        current_user = request.user
        test_status = TestStatus.objects.get(user=current_user,test=test_id)
        save_time(request,test_status)
        return HttpResponse(status=204)