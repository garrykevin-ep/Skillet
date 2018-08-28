from django.contrib.auth.models import User
from django.db import models

# TODO user test status
#  

class Test(models.Model):
	name =  models.CharField(max_length=50)
	minute = models.IntegerField()
	second = models.IntegerField()
	rules = models.TextField()
	questions_count = models.IntegerField(default=1)
	publish = models.BooleanField(default=False)# not used
	def __str__(self):
		return self.name

class TestStatus(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	test = models.ForeignKey(Test,on_delete = models.CASCADE)
	mark = models.IntegerField()
	minute = models.IntegerField()
	second = models.IntegerField()
	completed = models.BooleanField(default=False)

	class Meta:
		unique_together = (('user', 'test'),)

class Question(models.Model):
	test = models.ForeignKey(Test , on_delete = models.CASCADE)
	question_text = models.CharField(null = False,max_length= 200)
	code = models.TextField(blank=True)
	image = models.ImageField(blank=True)
	mark = models.IntegerField(default=1,blank=False)
	Question_Type = (
		('mcq','mcq'),
		('fill','fill'),
		)
	type = models.CharField(max_length=3,choices=Question_Type,default='mcq')
	
	def __str__(self):
		return self.question_text

class QuestionOrder(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	question = models.ForeignKey(Question, on_delete = models.CASCADE)

#multi choice manger 
class MultiChoiceManager(models.Manager):
	def get_queryset(self):
		return super(MultiChoiceManager,self).get_queryset().filter(type='mcq')

#proxy multi choice Question
class MultiQuestion(Question):
	objects = MultiChoiceManager()

	class Meta:
		verbose_name = 'Multiple Choice Questions'
		verbose_name_plural = 'Multiple Choice Questions'
		proxy = True    

#choice for multi
class MultiChoice(models.Model):
    question = models.ForeignKey(MultiQuestion, on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200,null = False)
    ans = (
    	('Yes', 'Yes'),
    	('No', 'No')
    	) 	
    answer = models.CharField(max_length=3,choices=ans,default='No')
    def __str__(self):
        return self.choice_text

class MultiStatus(models.Model):
	User = models.ForeignKey(User)
	question = models.ForeignKey(MultiQuestion)
	#red not answered,yellow ans but flag,ans green
	status = (
		('Red','red'),
		('Yellow','yellow'),
		('Green','green'),
		)
	#Question not answer first so red
	Qstatus = models.CharField(max_length=6,choices=status,default='red')
	selected = models.IntegerField(default=-1)
	#not answered -1,pre 1 or 0 not used in multi
	preResult  = models.IntegerField(default=-1)


#fill up manager
class FillManager(models.Manager):
	def get_queryset(self):
		return super(FillManager,self).get_queryset().filter(type='fill')
	
#proxy for fill ups	
class FillQuestion(Question):
	objects = FillManager()
	class Meta:
		verbose_name = "Fill Up"
		verbose_name_plural = "Fill Ups"	
		proxy = True

#substrings for fill ups
class FillChoice(models.Model):
	question = models.ForeignKey(FillQuestion,on_delete= models.CASCADE)
	choice_text = models.CharField(max_length=200,null = False)

class FillStatus(models.Model):
	User = models.ForeignKey(User)
	question = models.ForeignKey(FillQuestion)
	#red not answered,yellow ans but flag,ans green
	status = (
		('Red','red'),
		('Yellow','yellow'),
		('Green','green'),
		)
	#Question not answer first so red
	Qstatus = models.CharField(max_length=6,choices=status,default='red')
	answer = models.CharField(max_length=200,blank=True)
	#not answered -1,pre 1 or 0
	preResult  = models.IntegerField(default=-1)

#TODO 
	# class Meta:
	# 	unique_together = (('User', 'question'),)
