from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Login')
    email = forms.CharField(required=True, label='Email')
    nickname = forms.CharField(required=True, label='NickName')
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label='Repeat password', widget=forms.PasswordInput())
    avatar = forms.ImageField(required=True, label='Upload avatar')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'nickname',
            'password1',
            'password2',
            'avatar'
        ]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True, label='Login')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())


class QuestionFrom(forms.ModelForm):
    title = forms.CharField(required=True, label='Title')
    text = forms.CharField(required=True, max_length=960, widget=forms.Textarea)
    tags = forms.CharField(required=False, label='Tags')

    class Meta:
        model = Quest
        fields = [
            'title',
            'text'
        ]


class AnswerForm(forms.ModelForm):
    text = forms.CharField(required=True, max_length=960, widget=forms.Textarea(
        attrs={'placeholder': 'Enter your answer here.', 'class': 'answer-textfield'}))

    class Meta:
        model = Answer
        fields = [
            'text'
        ]
