from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from  django.urls import reverse
from django.shortcuts import get_object_or_404,render,get_list_or_404,redirect
from .models import Question,Choice,Status
from login.models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required(login_url = '/')
def s_pop(request):
    current_user = request.user
    qlist = Question.objects.all()
    for x in qlist:
        Status.objects.get_or_create(User = current_user,question = x)
    return HttpResponseRedirect(reverse('quiz:ans',args = (first_question(),)))

def no_of_Question():
    return len(Question.objects.all())

def first_question():
    list = Question.objects.all()
    list = list[0]
    return list.id

def last_question():
    list = Question.objects.all()
    len_lst = len(list)
    list = list[len_lst-1]
    return list.id

def next_question(pk):
    pk = int(pk)
    if pk != last_question():
        list = Question.objects.filter(id__gt = pk)
        list = list[0]
        return list.id
    else:
        return None

def prev_question(pk):
    pk = int(pk)
    if pk != first_question():
        list = Question.objects.filter(id__lt = pk) 
        len_lst  = len(list)
        list = list[len_lst-1]
        return list.id
    else:
        return None

@login_required(login_url = '/')
def ans(request,pk):
    current_user = request.user
    question = get_object_or_404(Question,pk=pk)
    status, created = Status.objects.get_or_create(User = current_user,question = question)
    #return HttpResponse(status)
    if request.method == 'POST':
        #when data is sent
        try:
            value = request.POST['choice']
            selected_choice = question.choice_set.get(pk = value)
        except(KeyError, Choice.DoesNotExist):
            status.selected = -1
            status.save()
        else:
            mark = UserProfile.objects.get(user = current_user.id)
            #ans is corect
            if(selected_choice.answer == 'Yes' ):
                #two times same correct answer
                if selected_choice.id != status.selected:
                    add_mark(mark)
            else:
                if status.selected != -1:
                    #not first time answering the question
                    pre_choice = Choice.objects.get(pk = status.selected)
                    if pre_choice.answer == 'Yes':
                        #wrong ans afer corect ans
                        dec_mark(mark)
            #ans first time
            status.selected = value
            status.save()                      
        return disp_next_question(question,pk)
    else:
        #get method
        return disp_question(request,pk,current_user,question)

def add_mark(mark):
    mark.mark += 1
    mark.save()

def dec_mark(mark):
    mark.mark -= 1 
    mark.save()

def disp_question(request,pk,current_user,question):
    #get request
    pre_question = prev_question(pk)
    current_status = Status.objects.get(User= current_user,question = question)
    status = get_list_or_404(Status,User = current_user)
    dic ={
    'question' : question,
    'first_question': first_question,
    'last_question' : last_question,
    'pre_question' : pre_question,
    'status'  : status,
    'current_status' : current_status,
    }
    return render(request,'quiz/index.html',dic)

def disp_next_question(question,pk):
    next_Question = next_question(pk)
    if(next_Question != None):
            return HttpResponseRedirect(reverse('quiz:ans',args = (next_Question,)))
    else:
        return redirect('login:logout')
        #return HttpResponse("Thank You") #need to check how many left unanswerd

def disp(request,pk): 
    list = Question.objects.all()
    len_lst = len(list)
    list = list[len_lst-1]
    return HttpResponse(next_question(pk))
    