from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from  django.urls import reverse
from django.shortcuts import get_object_or_404,render
from .models import Question,Choice,Mark

def index(request,pk):
    question  = get_object_or_404(Question,pk = pk)
    return render(request,'quiz/index.html',{'question' : question})

def no_of_Question():
    return len(Question.objects.all())

def ans(request,pk):
    question = get_object_or_404(Question,pk = pk)
    next_question = question.id + 1
    try:
         selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,'quiz/index.html', {'question': question,'error_message': "You did'nt select a choice"})
    else:
        if(selected_choice.answer == True):
            mark = get_object_or_404(Mark,pk = 1)
            mark.mark += 1
            mark.save()
    if(no_of_Question() >= next_question):
        return HttpResponseRedirect(reverse('quiz:index',args = (next_question,)))
    else:
        return HttpResponse("Thank You")