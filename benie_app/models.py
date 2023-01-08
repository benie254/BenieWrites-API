from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
import datetime as dt
from django.http import Http404

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=60,default='')

    def __str__(self):
        return self.tag_name

class Story(models.Model):
    author = models.CharField(max_length=120,default='')
    author_pic = models.URLField(max_length=1000,default='')
    cover = models.URLField(max_length=1000,default='')
    title = models.CharField(max_length=120,default='')
    description = models.TextField(max_length=5000,default='')
    CATEGORIES = (('short-story','short-story',),('novel','novel'),('novelette','novelette'),('play','play'),('flash-fiction','flash-fiction'))
    category = models.CharField(max_length=60,choices=CATEGORIES,default='')
    GENRES = (('mystery','mystery',),('drama','drama',),('thriller','thriller'),('drama','drama'),('mystery/thriller','mystery/thriller'),('action','action'),('romance','romance'),('teen-fiction','teen-fiction'))
    genre = models.CharField(max_length=60,choices=GENRES,default='')
    tagged = models.ManyToManyField(Tag,null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    first_published = models.DateField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    STATUSES = (('completed','completed'),('ongoing','ongoing'))
    status = models.CharField(max_length=60,choices=STATUSES,default='')
    PINS = (('pinned','pinned'),('unpinned','unpinned'))
    pin = models.CharField(choices=PINS,max_length=60,default='',null=True,blank=True)
    words = models.PositiveIntegerField(null=True,blank=True)
    likes = models.IntegerField(null=True,blank=True)
    comments = models.IntegerField(null=True,blank=True)
    chaps = models.IntegerField(null=True,blank=True)
    chap1_id = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=120,default='')
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='',null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    first_published = models.DateField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    words = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=120,default='')
    cover = models.URLField(max_length=1000,default='')
    description = models.TextField(max_length=5000,default='') 
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,default='',null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    words = models.PositiveIntegerField(null=True,blank=True)

    def __description__(self):
        return self.title

class Poem(models.Model):
    title = models.CharField(max_length=120,default='')
    cover = models.URLField(max_length=1000,default='')
    cover_source = models.URLField(max_length=50,default='')
    excerpt = models.TextField(max_length=2000,default='') 
    description = models.TextField(max_length=5000,default='') 
    uploaded = models.DateTimeField(auto_now_add=True)
    words = models.PositiveIntegerField(null=True,blank=True)
    CATEGORIES = (('Spoken-Word','Spoken-Word',),('Poetic-Chains','Poetic-Chains'),('Poetic-Notes','Poetic-Notes'),('One-Liners','One-Liners'),('Poems','Poems'))
    category = models.CharField(max_length=60,choices=CATEGORIES,default='')
    TAGS = (('love','love',),('life','life'))
    tag = models.CharField(max_length=60,choices=TAGS,default='',null=True,blank=True)
    STATUS = (('pinned','pinned'),('unpinned','unpinned'))
    status = models.CharField(choices=STATUS,max_length=60,default='',null=True,blank=True)
    likes = models.IntegerField(null=True,blank=True)

    def __description__(self):
        return self.title

    @classmethod 
    def search(cls, past_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
            # raise 404 when value error is thrown
            raise Http404()
            assert False
            
        poems = cls.objects.filter(uploaded__date=date)
        return poems

class Feedback(models.Model):
    comment = models.TextField(max_length=2500,null=True,blank=True,default='Beautiful piece!')
    commented_by = models.CharField(max_length=120,null=True,blank=True,default='Anonymous')
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,default='',null=True,blank=True)
    poem = models.ForeignKey(Poem,on_delete=models.CASCADE,default='',null=True,blank=True)
    likes = models.IntegerField(null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    replies = models.IntegerField(null=True,blank=True)


class Reaction(models.Model):
    REACTIONS = (('like','like'),('dislike','dislike'))
    like = models.CharField(choices=REACTIONS,max_length=60,default='',null=True,blank=True)
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='',null=True,blank=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,default='',null=True,blank=True)
    poem = models.ForeignKey(Poem,on_delete=models.CASCADE,default='',null=True,blank=True)
    comment = models.ForeignKey(Feedback,on_delete=models.CASCADE,default='',null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.like



class Reply(models.Model):
    msg = models.TextField(max_length=2500,null=True,blank=True,default='')
    replied_by = models.CharField(max_length=120,null=True,blank=True,default='')
    comment = models.ForeignKey(Feedback,on_delete=models.CASCADE,default='',null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

class Notification(models.Model):
    subject = models.CharField(max_length=60,default='',null=True,blank=True)
    message = models.CharField(max_length=1200,default='')
    date = models.DateTimeField(default=timezone.now)
    link = models.URLField(max_length=1000,null=True,blank=True)
    img = models.URLField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.subject

class Subscriber(models.Model):
    name = models.CharField(max_length=220,default='',null=True,blank=True)
    email = models.EmailField(max_length=220,default='',null=True,blank=True,unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=220,default='',null=True,blank=True)
    email = models.EmailField(max_length=220,default='',null=True,blank=True)
    message = models.TextField(max_length=9000,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


