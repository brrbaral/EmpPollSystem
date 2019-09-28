from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #ONE TO ONE BECAUSE OF ONE USER HAVE ONLY ON PROFILE
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    designation=models.CharField(max_length=20,null=True,blank=True)
    salary=models.IntegerField(null=True,blank=True)
    picture=models.ImageField(upload_to='images/%Y/%m/%d/',max_length=255,null=True)

    class Meta:
        ordering=['-salary'] #DESC ORDER

    def __str__(self):
        return "{0}{1}".format(self.user.first_name,self.user.last_name)
@receiver(post_save,sender=User) #POST_SAVE MEANS THE SIGNAL IS THROWN AFTER THE METHOD SAVE()
def user_is_created(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance) #INSTANCE IS A OBJECT OF USER TABLE
    else:
        instance.profile.save() #USER HAVE A ACCESS OF PROFILE CLASS DIRECTLY


#user=kwargs['instance']; kwargs is the user