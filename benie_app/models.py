from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=60,default='')

    def __str__(self):
        return self.tag_name

class Story(models.Model):
    author = models.CharField(max_length=120,default='')
    cover = models.URLField(max_length=1000,default='')
    title = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=5000,default='')
    CATEGORIES = (('mys','mystery',),('thr','thriller'),('dr','drama'),('mys/thr','mystery/thriller'),('act','action'),('rom','romance'))
    category = models.CharField(max_length=60,choices=CATEGORIES,default='')
    tagged = models.ManyToManyField(Tag,null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    first_published = models.DateField(default=timezone.now)
    STATUSES = (('com','completed'),('on','ongoing'))
    status = models.CharField(max_length=60,choices=STATUSES,default='')
    last_updated = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=5000,default='') 
    story = models.ForeignKey(Story,on_delete=models.DO_NOTHING,default='',null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    first_published = models.DateField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    like = models.BooleanField(default='',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.DO_NOTHING,default='')
    date = models.DateTimeField(default=timezone.now)

    def __bool__(self):
        return self.like

class Feedback(models.Model):
    comment = models.TextField(max_length=2500,null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.DO_NOTHING,default='')
    date = models.DateTimeField(default=timezone.now)

    def __bool__(self):
        return self.comment
