from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Categorys(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='static/img/cat', default="")
    
    def __str__(self):
        return self.name

# Create your models here.
class Posts(models.Model):
     sno= models.AutoField(primary_key=True)
     title= models.CharField(max_length=255)
     author= models.CharField(max_length=13)
     slug=models.CharField(max_length=130)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
     views = models.IntegerField(default=0)
     cat=models.ForeignKey(Categorys, on_delete=models.CASCADE,blank=True)
     img = models.ImageField(upload_to='static/img', default="")


     def __str__(self):
         return self.title + "by" + self.author


    

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now) 

    def __str__(self):
        return self.comment +" By "+self.user.username 
            
     