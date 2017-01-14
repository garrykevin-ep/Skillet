from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
	question_text = models.CharField(null = False,max_length= 200)
	def __str__(self):
		return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200,null = False)
    ans = (
    	('Yes', 'Yes'),
    	('No', 'No')
    	) 	
    answer = models.CharField(max_length=3,choices=ans,default='No')
    def __str__(self):
        return self.choice_text

class Status(models.Model):
	User = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	#red not answered,yellow ans but flag,ans green
	status = (
		('Red','red'),
		('Yellow','yellow'),
		('Green','green'),
		)
	#Question not answer first so red
	Qstatus = models.CharField(max_length=6,choices=status,default='red')
	selected = models.IntegerField(default=-1)
	#p_correct = models.BooleanField(default=False)