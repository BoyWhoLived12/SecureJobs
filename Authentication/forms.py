# from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django import forms


class CreateUserForm(UserCreationForm):
    choices = (
        ('p', 'personal'),
        ('c', 'company')
    )
    accType = forms.ChoiceField(label='account type', choices=choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'accType', 'password1', 'password2']
