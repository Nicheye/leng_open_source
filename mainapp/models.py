from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
class table(models.Model):
    created_by = models.ForeignKey(User,related_name='created_tables',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name   
class Profile(models.Model):
    user =models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
    nickname = models.CharField(max_length=25,default=None,null=True)
    in_queue = models.BooleanField(default=False)
    elo = models.IntegerField(default=1000)
    ava = models.ImageField(upload_to='avatars',default="/static/images/userlogodefault.jpg")
    background = models.ImageField(upload_to="backgrounds",default="/static/images/userlogodefault.jpg")
    password = models.CharField(max_length=50,default=None,null=True)
    def __str__(self):
        return str(self.user)
class word(models.Model):
    created_by = models.ForeignKey(User,related_name='created_words',on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    wordineng=models.CharField(max_length=100)
    table = models.ForeignKey(table,related_name="table",on_delete=models.CASCADE)
    def __str__(self):
        return self.word
class FeedBack(models.Model):
    name = models.CharField(max_length=100)
    phone =models.CharField(max_length=60)
    message= models.CharField(max_length=1000)

class Follow(models.Model):
    follow_to = models.ForeignKey(User,related_name='followed_to',on_delete=models.CASCADE)
    follow_by = models.ForeignKey(User,related_name='followed_by',on_delete=models.CASCADE)
