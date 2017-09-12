from difflib import SequenceMatcher

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.urls import reverse

from login.models import UserProfile

from coding.views import answer_coding,coding_display
from coding.models import CodeUserStatus

from .models import *

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# navigation helper functions
def no_of_Question():
    return len(Question.objects.all())

def first_question():
    list = Question.objects.all()
    list = list[0]
    return list

def last_question():
    list = Question.objects.all()
    len_lst = len(list)
    list = list[len_lst-1]
    return list

def next_question(pk):
    pk = int(pk)
    if pk != last_question().id:
        list = Question.objects.filter(id__gt = pk)
        list = list[0]
        return list
    else:
        return None

def prev_question(pk):
    pk = int(pk)
    if pk != first_question().id:
        list = Question.objects.filter(id__lt = pk) 
        len_lst  = len(list)
        len_lst = len_lst-1
        list = list[len_lst]
        return list
    else:
        return None

def nth_question(pk):
    qlist = Question.objects.all()
    pk = int(pk)
    pk = pk -1
    return qlist[pk]

#question helper functions
def add_mark(mark):
    mark.mark += 1
    mark.save()

def dec_mark(mark):
    mark.mark -= 1 
    mark.save()

def save_time(request,user):
    #user is userprofile object
    if user.rmin >= request.POST['min']:  
        user.rmin = request.POST['min']
        user.rsec = request.POST['sec']
        user.save()

# get correct ans
def get_ans_multi(question):
    list = MultiChoice.objects.filter(question=question)
    for x in list:
        if x.answer == 'Yes':
            return x.id

def get_current_status(question,current_user):
    if question.type == 'mcq':
        return MultiStatus.objects.get(User= current_user,question = question)
    elif question.type == 'fill':
        return FillStatus.objects.get(User= current_user,question = question)

def get_choices(question):
    if question.type == 'mcq':
        return MultiChoice.objects.filter(question=question)
    elif question.type == 'fill':
        return FillChoice.objects.filter(question=question)

def get_all_status(current_user):
    mcq_list = MultiStatus.objects.filter(User=current_user)
    fill_list  = FillStatus.objects.filter(User=current_user)
    full = list(mcq_list)+list(fill_list)
    full =  sorted(full,key=lambda x: x.question.id)
    return full

def is_fill_correct(question,currentAnswer):
    #checks similar if matches > .5 correct
    options = get_choices(question)
    for x in options:
        if similar(currentAnswer,x.choice_text) > .5:
            return  True
    return False

    
# main functions , post hits here
@login_required(login_url = '/')
def s_pop(request):
    current_user = request.user
    qlist = Question.objects.all()
    for x in qlist:
        if x.type == 'mcq':
           MultiStatus.objects.get_or_create(User = current_user,question = x)
        elif x.type == 'fill':
           FillStatus.objects.get_or_create(User=current_user,question= x)
        elif x.type == 'code':
            CodeUserStatus.objects.get_or_create(User=current_user,question= x)
    return redirect('quiz:rule')
    return HttpResponseRedirect(reverse('quiz:disp',args = (first_question().id,)))


@login_required(login_url = '/')
def disp(request,pk):
    question = get_object_or_404(Question,pk=pk)
    current_user = request.user
    if request.method == 'POST':
        nav = request.POST['nav']
        ans(request,pk)
        if nav == 'submit':
            return answer_coding(request,pk,question)
        elif nav  == 'Next' or nav == 'Finish':
            #function is just to check last question
            return disp_next_question(question,pk)
        elif nav == 'Previous':
            prev_q = prev_question(pk)
            return HttpResponseRedirect(reverse('quiz:disp',args = (prev_q.id,)))
        else:
            nth_q = nth_question(nav)
            return HttpResponseRedirect(reverse('quiz:disp',args = (nth_q.id,)))
    else:
        return disp_question(request,pk,current_user,question)

@login_required(login_url = '/')
#actually ans post always
def ans(request,pk):
    current_user = request.user
    question = get_object_or_404(Question,pk=pk)
    status = get_current_status(question,current_user)
    user = UserProfile.objects.get(user = current_user.id)
    status.Qstatus = request.POST['status']
    status.save()
    save_time(request,user)
    if question.type == 'mcq':
        answer_multi(request,question,user,status)
    elif question.type == 'fill':
        answer_fill(request,user,question,status)

def answer_fill(request,user,question,status):
    currentAnswer = request.POST['answer']
    # fill is blank
    if currentAnswer == '':
        #last ans is correct
        if status.preResult != -1:  
            dec_mark(user)
        status.preResult = -1
        status.save()
    else:
        # fill not blank,ans is correct
        if is_fill_correct(question,currentAnswer):
            #two times correct answer
            if status.preResult != 1:
                add_mark(user)
                status.preResult = 1
                status.save()
        else:
            if status.preResult == 1:
                #not first time answering the question
                #wrong answer after correct ans
                dec_mark(user)
                status.preResult = 0
                status.save()
    status.answer = currentAnswer
    status.save()


def answer_multi(request,question,user,status):
    try:
        value = request.POST['choice']
        selected_choice = MultiChoice.objects.get(pk=value)
    except:
        # last ans is correct , no choice selected now
        if status.selected == get_ans_multi(question):
            dec_mark(user)
        status.selected = -1
        status.save()   
    else: 
        #ans is correct , choice is selected
        if(selected_choice.answer == 'Yes' ):
            #two times same correct answer
            if selected_choice.id != status.selected:
                add_mark(user)
        else:
            if status.selected != -1:
                #not first time answering the question
                pre_choice = MultiChoice.objects.get(pk = status.selected)
                if pre_choice.answer == 'Yes':
                    #wrong ans afer corect ans
                    dec_mark(user)
        #ans first time
        status.selected = value
        status.save()



def disp_question(request,pk,current_user,question):
    if question.type == 'mcq' or question.type == 'fill':
        return multi_fill_display(request,pk,current_user,question)
    elif question.type == 'code':
        dic = {}
        return coding_display(request,pk,question)

def multi_fill_display(request,pk,current_user,question):
    #get request
    #can display multi choice or fillups
    pre_question = prev_question(pk)
    current_status = get_current_status(question,current_user)
    user = UserProfile.objects.get(user = current_user.id)
    dic ={
    'question' : question,
    'first_question': first_question,
    'last_question' : last_question,
    'pre_question' : pre_question,
    'next_question': next_question,
    #status for displaying status of other questions
    'status'  : get_all_status(current_user),
    'choice' : get_choices(question),
    'current_status' : current_status, 
    'user' : user,
   }
    return render(request,'quiz/index.html',dic)

def disp_next_question(question,pk):
    next_Question = next_question(pk)
    if(next_Question != None):
            return HttpResponseRedirect(reverse('quiz:disp',args = (next_Question.id,)))
    else:
        return HttpResponseRedirect(reverse('quiz:end',args = (pk,)))

def timer(request):
    if request.method == 'POST':
        current_user = request.user
        user = UserProfile.objects.get(user = current_user.id)
        save_time(request,user)
        return HttpResponse(status=204)

def end(request,pk):
    dic = {
    'pk' : pk,
    }
    return render(request,'quiz/end.html',dic)

@login_required(login_url = '/')
def rules(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz:disp',args = (first_question().id,)))
    else:
         dic  = {
         'user' : request.user.id,
         }  
         return render(request,'quiz/rules.html',dic)
