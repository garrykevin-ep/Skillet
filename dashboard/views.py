from django.shortcuts import render
from django.http import HttpResponse
from .models import nav_drop_down,card
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from .config import *

# Create your views here.
@login_required(login_url = '/')
def dashboard(request):
	nav = nav_drop_down.objects.all()
	cards = card.objects.all()
	current_user = request.user
	context = {
	'nav': nav,
	'card':cards,
	'user' : current_user,
	}
	return render(request,'dashboard/index.html',context)