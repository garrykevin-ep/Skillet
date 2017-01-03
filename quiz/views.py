from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from  django.urls import reverse
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth import authenticate,login
from .models import Question,Choice
from login.models import UserProfile

def auth_login(request):
    return render(request,'login/login.html')

def auth(request):
    user_name = request.POST['user_name']
    pasword = request.POST['password']
    User = authenticate(username = user_name , password = pasword )
    if User is not None:
            if User.is_active:
                login(request,User)
                return HttpResponseRedirect(reverse('quiz:index',args = (1,)))
    else:
        return render(request,'login/login.html',{'error_message' : "Wrong Pass",
                                                  'x' : pasword})

def index(request,pk):
    question  = get_object_or_404(Question,pk = pk)
    return render(request,'quiz/index.html',{'question' : question})

def no_of_Question():
    return len(Question.objects.all())

def ans(request,pk):
    question = get_object_or_404(Question,pk = pk)
    next_question = question.id + 1
    current_user = request.user
    try:
         selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,'quiz/index.html', {'question': question,'error_message': "You did'nt select a choice"})
    else:
        mark = UserProfile.objects.get(user = current_user.id)
        if(selected_choice.answer == True):
            mark.mark += 1
            mark.save()
    if(no_of_Question() >= next_question):
        return HttpResponseRedirect(reverse('quiz:index',args = (next_question,)))
    else:
        return HttpResponse("Thank You")