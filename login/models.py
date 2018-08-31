from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


#To save mark and ph_no a user
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name= 'profile',on_delete=models.CASCADE,primary_key=True)
    ph_no = models.CharField(blank=True,null = True,max_length=50)
    email = models.CharField(blank=True,null=True,max_length=200)
    college = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
    	return 'user {}'.format(self.user.username)
        # return 'Profile of user: {} -- mark = {} '.format(self.user.username,self.mark)

#To populate when a user is registered
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
#used signal 
post_save.connect(create_user_profile, sender=User)
