from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Please enter a valid email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class DebugInputForm(forms.Form):
    params_input = forms.CharField(max_length=100)
    debug_input = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))

class TestCaseForm(forms.ModelForm):
    test_input = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))
    expected_output = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))

    class Meta:
        model = TestCase
        fields = ('__all__')

class TestCaseProgramForm(forms.ModelForm):
    test_input = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))
    expected_output = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))

    class Meta:
        model = TestCaseProgram
        fields = ('__all__')

class TestCaseFunctionForm(forms.ModelForm):
    test_input = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))
    expected_output = forms.CharField(max_length=500, widget=forms.Textarea({'rows': 2, 'cols': 30}))

    class Meta:
        model = TestCaseFunction
        fields = ('__all__')