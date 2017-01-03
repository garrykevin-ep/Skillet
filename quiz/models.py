from django.db import models


class Question(models.Model):
    question_text = models.CharField(null = False,max_length= 200)
    code_text = models.TextField(null = True,blank= True)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200,null = False)
    answer = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
