from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#To save mark and ph_no a user
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name= 'profile')
    mark = models.IntegerField(default= 0)
    ph_no = models.IntegerField(max_length=10,null = True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

#To populate when a user is registered
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
#used signal 
post_save.connect(create_user_profile, sender=User)