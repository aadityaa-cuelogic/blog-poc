from django.contrib.auth.forms import AuthenticationForm
from django import forms

import re
from django.contrib.auth.models import User
from .models import Post, Category
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
# If you don't do this you cannot use Bootstrap CSS

class CreatePostForm(forms.Form):
    title = forms.RegexField(regex=r'^[a-zA-Z0-9_\-\s]+$',
            widget=forms.TextInput(attrs={'required':True, 'max_length':200,
            'class':"form-control", 'placeholder': 'Enter title for your post'}),
            label=_("Title"),
            error_messages={ 'invalid':
            _("Title can contain only letters,numbers,underscores and space.")})
    category = forms.ModelChoiceField(queryset=(Category.objects.all()),
                label=_("Category")
                )
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'required':True,
                'max_length':200,'class':"form-control",
                'placeholder': 'Enter description for your post'}),
            label=_("Description"))
    file_field = forms.FileField(widget=forms.ClearableFileInput(
            attrs={'multiple': False}),
            label=_("Upload Image"),
            required=False)

    def clean_title(self):
        try:
            post = Post.objects.get(title__iexact=self.cleaned_data['title'])
        except Post.DoesNotExist:
            return self.cleaned_data['title']
        raise forms.ValidationError(
            _("This post title already exits. Please try something else!"))

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                    widget=forms.TextInput(attrs={'class': 'form-control',
                    'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                    widget=forms.PasswordInput(
                        attrs={'class': 'form-control', 'name': 'password'}))


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[a-z0-9_-]{3,15}$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Username"), error_messages={ 'invalid':
        _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True,
        max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=
        dict(required=True, max_length=30, render_value=False)),
         label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=
        dict(required=True, max_length=30, render_value=False)),
         label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            _("The username already exists. Please try another one."))

    def clean_email(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(
            _("The email already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
