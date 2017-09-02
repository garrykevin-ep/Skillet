from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from quiz.models import Question

from .form import RegisterForm
#user defined
from .models import UserProfile


def auth_login(request):
    return render(request,'login/login.html')

def auth(request):
    user_name = request.POST['user_name']
    pasword = request.POST['password']
    User = authenticate(username = user_name , password = pasword )
    if User is not None:
            if User.is_active:
                login(request,User)
                return redirect('quiz:pop')
                #return HttpResponseRedirect(reverse('quiz:ans',args = (first_question(),)))
    else:
        return render(request,'login/login.html',{'error_message' : "Wrong Password or You finished the test",
                                                  'x' : pasword})
def register(request):
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid(): #need to check if user alredy exist NEED TO 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            #if user not exist create a user
            user = User.objects.create_user(username = username)
            user.set_password(password)
            user.save()
            
            #save phone number of a user 
            number = form.cleaned_data['phone']
            ph_save(user,number)
            
            #login and redirect to main page
            auth = authenticate(username = username ,password = password)
            login(request,auth)
            return redirect('quiz:pop')
            #return HttpResponseRedirect(reverse('quiz:index',args = (1,)))
        else:
            #when form data is wrong
            form = RegisterForm()
            return render(request,'login/register.html',{'error_message' : "not vaild username",'form' : form})   
    else:
        #if just display page
        form = RegisterForm()
        return render(request,'login/register.html', {'form' : form})

#save phone number of a user
def ph_save(user,number):
    usr_pro = UserProfile.objects.get(user = user.id)
    usr_pro.ph_no = number
    usr_pro.save()

def first_question():
    list = Question.objects.all()
    list = list[0]
    return list.id

def logout_view(request):
    current_user  = request.user
    a = User.objects.get(id= current_user.id)
    # a.is_active = False
    a.save() 
    logout(request)
    return redirect('login:login')
