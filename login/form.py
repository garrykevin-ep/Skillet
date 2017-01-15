from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RegisterForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	phone = forms.CharField(widget=forms.TextInput(attrs=dict(required=True)),  label=_("Phone Number"))
	password1 = forms.IntegerField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
	#password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))