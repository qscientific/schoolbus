from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bus_tracker.models import Profile

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_OPTIONS, help_text='Required. Please choose your user type')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')