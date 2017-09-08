from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from quiz.models import Question

# Create your models here.

class CodeManager(models.Manager):
	def get_queryset(self):
		return super(CodeManager,self).get_queryset().filter(type='code')

class CodeQuestion(Question):
	objects = CodeManager()

	class Meta:
		verbose_name = 'Coding Question'
		verbose_name_plural = 'Coding Questions'
		proxy = True

class CodeTestCase(models.Model):
	question = models.ForeignKey(CodeQuestion,on_delete= models.CASCADE)
	input = models.TextField()
	output = models.TextField()

class CodeQuestionExtend(models.Model):
	question = models.OneToOneField(CodeQuestion,on_delete= models.CASCADE)
	problem_statement = models.TextField()
	input_statement = models.TextField()
	output_statement = models.TextField()
	constraint = models.TextField()
	explanation = models.TextField() 
	testcase_file = models.FileField(upload_to='testcases')
	answer_file = models.FileField(upload_to='answers')
	lines_per_testcase = models.IntegerField(default=1)
	lines_per_answer = models.IntegerField(default=1)

class CodeUserStatus(models.Model):
	User = models.ForeignKey(User)
	question = models.ForeignKey(CodeQuestion)
	status = (
		('Accepted','Accepted'),
		('Not Accepted','Not Accepted'),
		)
	question_status = models.CharField(max_length=15,choices=status,default='Not Accepted')
	remaining_time = models.IntegerField(blank=True,null=True)
		
class UserSubmission(models.Model):
	User = models.ForeignKey(User,on_delete= models.CASCADE)
	question = models.ForeignKey(CodeQuestion,on_delete= models.CASCADE)
	failed_testcase = models.TextField(blank=True,null=True)
	expected_output = models.TextField(blank=True,null=True)
	user_output = models.TextField(blank=True,null=True)
	ith_test_case_failed = models.IntegerField(blank=True,null=True)
	rmin = models.IntegerField()
	rsec = models.IntegerField()