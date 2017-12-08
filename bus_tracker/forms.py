from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bus_tracker.models import Profile

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_OPTIONS, help_text='Required. Please choose your user type')
    geo_long = forms.FloatField(help_text='click on map!')
    geo_lat = forms.FloatField(help_text='click on map!')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type', 'geo_long', 'geo_lat')