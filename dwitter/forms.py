from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

from .models import Dweet


class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=CKEditorWidget())

    class Meta:
        model = Dweet
        exclude = ("user",)


class DweetFormCK(forms.ModelForm):
    body = forms.CharField(required=True, widget=CKEditorWidget())

    class Meta:
        model = Dweet
        fields = '__all__'


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name:')
    email = forms.EmailField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100, help_text='First Name', label='First Name :')
    last_name = forms.CharField(max_length=100, help_text='Last Name', label='Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
