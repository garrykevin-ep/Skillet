from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


#To save mark and ph_no a user
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name= 'profile',on_delete=models.CASCADE,primary_key=True)
    college_name = models.CharField(max_length=30)
    mark = models.IntegerField(default= 0)
    ph_no = models.CharField(max_length=30)
    rmin = models.CharField(null=True,max_length=2,default=50)
    rsec = models.CharField(null=True,max_length=2,default=10)
    def __str__(self):
        return 'Profile of user: {} -- mark = {} '.format(self.user.username,self.mark)

#To populate when a user is registered
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
#used signal 
post_save.connect(create_user_profile, sender=User)
