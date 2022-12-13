from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=60)

class Story(models.Model):
    cover = CloudinaryField('Story Cover')
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)
    CATEGORIES = (('mystery','mystery',),('thriller','thriller'),('drama','drama'),('mystery/thriller','mystery/thriller'),('action','action'),('romance','romance'))
    category = models.CharField(max_length=60,choices=CATEGORIES)
    tagged = models.ManyToManyField(Tag)

class Chapter(models.Model):
    cover = CloudinaryField('Chapter Cover',null=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=5000) 
    Story = models.ForeignKey(Story,on_delete=models.CASCADE)