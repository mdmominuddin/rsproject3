from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import FileAnalysis

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class FileAnalysisForm(forms.ModelForm):
    class Meta:
        model = FileAnalysis
        fields = ['user','projectname','filename','remark','uploadfile']
        widgets = {
            'projectname': forms.TextInput(attrs={'class': 'form-control'}),
            'filename': forms.TextInput(attrs={'class': 'form-control'}),

            'remark': forms.TextInput(attrs={'class': 'form-control'}),
            'uploadfile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
