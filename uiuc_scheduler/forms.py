from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First Name', 'style':'width:130px;'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name', 'style':'width:130px;'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = PasswordInput(attrs={'placeholder': 'Email Address'})
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Password Confirmation'})

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        
        return user
