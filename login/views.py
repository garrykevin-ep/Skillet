from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse
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
                return HttpResponseRedirect(reverse('quiz:index',args = (1,)))
    else:
        return render(request,'login/login.html',{'error_message' : "Wrong Pass",
                                                  'x' : pasword})
