from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

# Create your models here.

class User(AbstractUser):
    phone=models.CharField(max_length=15)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=10,null=True,blank=True)
    def generate_otp(self):
        otp_number=str(randint(1000,9000))+str(self.id)
        self.otp=otp_number
        self.save()


class Profile(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="userprofile")
    bio=models.CharField(max_length=300)
    address=models.TextField(null=True)
    photo=models.ImageField(upload_to="profile_picture",default="profile_picture/default.png")


from django.db.models.signals import post_save

def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile,User)
