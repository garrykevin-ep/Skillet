from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

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

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name= 'profile')
    mark = models.IntegerField(default= 0)
    ph_no = models.IntegerField(max_length=10,null = True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)