from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=60,default='')

    def __str__(self):
        return self.tag_name

class Story(models.Model):
    cover = CloudinaryField('Story Cover',default='')
    title = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=5000,default='')
    CATEGORIES = (('mystery','mystery',),('thriller','thriller'),('drama','drama'),('mystery/thriller','mystery/thriller'),('action','action'),('romance','romance'))
    category = models.CharField(max_length=60,choices=CATEGORIES,default='')
    tagged = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    cover = CloudinaryField('Chapter Cover',null=True)
    title = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=5000,default='') 
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='')

    def __str__(self):
        return self.title

class Reaction(models.Model):
    like = models.BooleanField(default='',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,default='')

    def __bool__(self):
        return self.like
