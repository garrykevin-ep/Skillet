from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import UserProfile


class RegisterForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	college_name = forms.CharField()
	phone = forms.CharField()
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))