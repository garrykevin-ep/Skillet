from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from  django.urls import reverse
from django.shortcuts import get_object_or_404,render,get_list_or_404,redirect
from .models import *
from login.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@login_required(login_url = '/')
def s_pop(request):
    current_user = request.user
    qlist = Question.objects.all()
    for x in qlist:
        if x.type == 'mcq':
           MultiStatus.objects.get_or_create(User = current_user,question = x)
        elif x.type == 'fill':
           FillStatus.objects.get_or_create(User=current_user,question= x)
    return HttpResponseRedirect(reverse('quiz:disp',args = (first_question().id,)))

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
    
# post hits here
@login_required(login_url = '/')
def disp(request,pk):
    question = get_object_or_404(Question,pk=pk)
    current_user = request.user
    if request.method == 'POST':
        nav = request.POST['nav']
        ans(request,pk)
        if nav  == 'Next' or nav == 'Finish':
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
    status = getCurrentStatus(question,current_user)
    user = UserProfile.objects.get(user = current_user.id)
    status.Qstatus = request.POST['status']
    status.save()
    saveTime(request,user)
    if question.type == 'mcq':
        answerMulti(request,question,user,status)
    elif question.type == 'fill':
        answerFill(request,user,question,status)

def answerFill(request,user,question,status):
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
        if isFillCorrect(question,currentAnswer):
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

def isFillCorrect(question,currentAnswer):
    #checks similar if matches > .5 correct
    options = getChoices(question)
    for x in options:
        if similar(currentAnswer,x.choice_text) > .5:
            return  True
    return False


def answerMulti(request,question,user,status):
    try:
        value = request.POST['choice']
        selected_choice = MultiChoice.objects.get(pk=value)
    except:
        # last ans is correct , no choice selected now
        if status.selected == getAnsMulti(question):
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


def add_mark(mark):
    mark.mark += 1
    mark.save()

def dec_mark(mark):
    mark.mark -= 1 
    mark.save()

# correct ans
def getAnsMulti(question):
    list = MultiChoice.objects.filter(question=question)
    for x in list:
        if x.answer == 'Yes':
            return x.id

def getCurrentStatus(question,current_user):
    if question.type == 'mcq':
        return MultiStatus.objects.get(User= current_user,question = question)
    elif question.type == 'fill':
        return FillStatus.objects.get(User= current_user,question = question)

def getChoices(question):
    if question.type == 'mcq':
        return MultiChoice.objects.filter(question=question)
    elif question.type == 'fill':
        return FillChoice.objects.filter(question=question)

def getAllStatus(current_user):
    mcq_list = MultiStatus.objects.filter(User=current_user)
    fill_list  = FillStatus.objects.filter(User=current_user)
    full = list(mcq_list)+list(fill_list)
    full =  sorted(full,key=lambda x: x.question.id)
    return full

def disp_question(request,pk,current_user,question):
    if question.type == 'mcq' or question.type == 'fill':
        return multiFillDisplay(request,pk,current_user,question)

def multiFillDisplay(request,pk,current_user,question):
    #get request
    #can display multi choice or fillups
    pre_question = prev_question(pk)
    current_status = getCurrentStatus(question,current_user)
    user = UserProfile.objects.get(user = current_user.id)
    dic ={
    'question' : question,
    'first_question': first_question,
    'last_question' : last_question,
    'pre_question' : pre_question,
    'next_question': next_question,
    #status for displaying status of other questions
    'status'  : getAllStatus(current_user),
    'choice' : getChoices(question),
    'current_status' : current_status, 
    'user' : user,
   }
    return render(request,'quiz/index.html',dic)

def disp_next_question(question,pk):
    next_Question = next_question(pk)
    if(next_Question != None):
            return HttpResponseRedirect(reverse('quiz:disp',args = (next_Question.id,)))
    else:
        return redirect('login:logout')
        #return HttpResponse("Thank You") #need to check how many left unanswerd

def timer(request):
    if request.method == 'POST':
        current_user = request.user
        user = UserProfile.objects.get(user = current_user.id)
        saveTime(user)
        return HttpResponse(status=204)
        

def saveTime(request,user):
    #user is userprofile object
    if user.rmin >= request.POST['min']:  
        user.rmin = request.POST['min']
        user.rsec = request.POST['sec']
        user.save()
