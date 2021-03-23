from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    DESIGNATION_CHOICES=[
        ("TEACHER","Teacher"),
        ("STUDENT","Student"),
    ]
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=False)
    designation=models.CharField(max_length=50,choices=DESIGNATION_CHOICES,default="STUDENT")
    
    
    def __str__(self):
        return "{} profile".format(self.user.username)

    def save(self):
        super().save()
        img=Image.open(self.profile_pic.path)

        if img.height>300 and img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)