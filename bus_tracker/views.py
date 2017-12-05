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
            user.profile.user_type = form.cleaned_data.get('user_type')
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

@login_required
def load_locations(request):
	logging.warning(request.method)
	logging.warning(request.user)
	logging.warning(request.user.profile)
	logging.warning(request.user.profile.user_type)
	if request.method == 'POST' and request.user.profile.user_type == Profile.DRIVER_TYPE:
		driver_location = [request.user.username, request.user.profile.geo_lat, request.user.profile.geo_long, 1]
		all_students = list(User.objects.filter(profile__user_type=Profile.STUDENT_TYPE))
		all_locations = map(lambda (i, x): [x.username, x.profile.geo_lat, x.profile.geo_long, i + 2], enumerate(all_students))
		all_locations.insert(0, driver_location)
		return JsonResponse({'success': True, 'locations': all_locations})
