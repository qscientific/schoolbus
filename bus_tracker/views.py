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
            user.profile.geo_long = form.cleaned_data.get('geo_long')
            user.profile.geo_lat = form.cleaned_data.get('geo_lat')
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
    if request.user.profile.user_type == Profile.DRIVER_TYPE:
        return render(request, 'home.html')
    elif request.user.profile.user_type == Profile.STUDENT_TYPE:
        return render(request, 'home2.html', {'student_username': request.user.username})

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
        try:
            school = User.objects.get(profile__user_type=Profile.ADMIN_TYPE)
            school_location = [school.username, school.profile.geo_lat, school.profile.geo_long, len(all_locations) + 1]
            all_locations.append(school_location)
        except: pass
        return JsonResponse({'success': True, 'locations': all_locations})
    if request.method == 'POST' and request.user.profile.user_type == Profile.STUDENT_TYPE:
        all_locations = []
        try:
            driver = User.objects.get(profile__user_type=Profile.DRIVER_TYPE)
            driver_location = [driver.username, driver.profile.geo_lat, driver.profile.geo_long, len(all_locations) + 1]
            all_locations.append(driver_location)
        except: pass
        all_students = list(User.objects.filter(profile__user_type=Profile.STUDENT_TYPE))
        all_studs_locations = map(lambda (i, x): [x.username, x.profile.geo_lat, x.profile.geo_long, i + 2], enumerate(all_students))
        all_locations.extend(all_studs_locations)
        try:
            school = User.objects.get(profile__user_type=Profile.ADMIN_TYPE)
            school_location = [school.username, school.profile.geo_lat, school.profile.geo_long, len(all_locations) + 1]
            all_locations.append(school_location)
        except: pass
        return JsonResponse({'success': True, 'locations': all_locations})
    else:
        return JsonResponse({'success': False})

@login_required
def update_locations(request):
    if request.method == 'POST' and request.user.profile.user_type == Profile.DRIVER_TYPE:
        logging.warning(request.POST)
        data = request.POST
        if type(data) != type(dict()): # could be a QueryDict
            data = dict(data)
            for k in data: # data is (k, [V]), make it (k, V)
                data[k] = data[k][0]
        try:
            request.user.profile.geo_long = data['longitude']
            request.user.profile.geo_lat = data['latitude']
            request.user.profile.save()
            return JsonResponse({'success': True});
        except:
            return JsonResponse({'success': False});

    else:
        return JsonResponse({'success': False});
