from django import forms

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
 
from .models import MyUser 
from django import forms
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.forms import UsernameField,ReadOnlyPasswordHashField 



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = MyUser
        fields = "__all__"
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

class MyRegForm(RegistrationForm):
    class Meta:
        model = MyUser
        fields = ('username','first_name','last_name','email',)
