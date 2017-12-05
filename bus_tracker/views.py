# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from bus_tracker.forms import SignUpForm
from bus_tracker.models import *
import logging



# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.sex = form.cleaned_data.get('sex')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.weight = form.cleaned_data.get('weight')
            user.profile.height = form.cleaned_data.get('height')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    return render(request, 'home.html')