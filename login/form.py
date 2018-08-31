from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import UserProfile


class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("Team name"))
	college = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("college name"))
	email = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("email"))
	phone = forms.IntegerField(widget=forms.NumberInput(attrs=dict(required=True,max_length=10)),  label=_("Phone Number"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
