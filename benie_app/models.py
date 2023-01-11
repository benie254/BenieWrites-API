from django.db import models
from django.utils import timezone
import datetime as dt
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from rest_framework.authtoken.models import Token

# Create your models here.
from django.dispatch import receiver
from django.core.mail import send_mail 

# Create your models here.
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
            """
            Create and save a user with the given username, email, and password.
            """
            # if not username:
            #     raise ValueError("The given username must be set")

            # if username is None:
            #     raise TypeError('Users must have a username.')

            # if email is None:
            #     raise TypeError('Users must have an email address.')

            email = self.normalize_email(email)
            # Lookup the real model class from the global app registry so this
            # manager method can be used in migrations. This is fine because
            # managers are by definition working on the real model.
            GlobalUserModel = apps.get_model(
                self.model._meta.app_label, self.model._meta.object_name
            )
            username = GlobalUserModel.normalize_username(username)
            user = self.model(username=username, email=email, **extra_fields)
            user.password = make_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise TypeError('Admins must have a password.')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    # A few helper functions for common logic between User and AnonymousUser.
    def _user_get_permissions(user, obj, from_name):
        permissions = set()
        name = "get_%s_permissions" % from_name
        for backend in auth.get_backends():
            if hasattr(backend, name):
                permissions.update(getattr(backend, name)(user, obj))
        return permissions


    def _user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_perm"):
                continue
            try:
                if backend.has_perm(user, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False


    def _user_has_module_perms(user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_module_perms"):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False

class MyUser(AbstractBaseUser,PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_(
            "Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with this username already exists."),
        }
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(
        _("email address"),unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        }
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyAccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email','first_name','last_name']


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Password(models.Model):
    username = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(max_length=120,null=True,blank=True)


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
    GENRES = (('mystery','mystery',),('drama','drama',),('thriller','thriller'),('drama','drama'),('mystery-thriller','mystery-thriller'),('action','action'),('romance','romance'),('teen-fiction','teen-fiction'))
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
    cover_source = models.URLField(max_length=50,default='',null=True,blank=True)
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
    story = models.ForeignKey(Story,on_delete=models.CASCADE,default='',null=True,blank=True)
    poem = models.ForeignKey(Poem,on_delete=models.CASCADE,default='',null=True,blank=True)

    def __int__(self):
        return self.pk

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


