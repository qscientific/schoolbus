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

from django.utils import timezone

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.user_type = Profile.STUDENT_TYPE
            user.profile.geo_long = form.cleaned_data.get('geo_long')
            user.profile.geo_lat = form.cleaned_data.get('geo_lat')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            attendance = Attendance(student=user.profile)
            attendance.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def gen_info(attendance_list, num_days_old):
    if(len(attendance_list) > num_days_old):
        attendance = attendance_list[num_days_old]
        if (not attendance.going): return "Skipped"
        elif (attendance.picked_time is None): return "Not Picked"
        else: return "Picked at " + str(attendance.picked_time.strftime('%H:%M:%S'))
    else:
        return "No Record"




@login_required
def home(request):
    if request.user.profile.user_type == Profile.DRIVER_TYPE:
        return render(request, 'home.html')
    elif request.user.profile.user_type == Profile.STUDENT_TYPE:
        return render(request, 'home2.html', {'student_username': request.user.username})
    elif request.user.profile.user_type == Profile.ADMIN_TYPE:
        data = request.GET
        if type(data) != type(dict()): # could be a QueryDict
            data = dict(data)
            for k in data: # data is (k, [V]), make it (k, V)
                data[k] = data[k][0]
        logging.warning(data)
        if 'days_old' in data:
            num_days_old = int(data['days_old'])
        else:
            num_days_old = 0;
        all_students = list(User.objects.filter(profile__user_type=Profile.STUDENT_TYPE))
        all_attendance = map(lambda x: (x.username,list(x.profile.attendance_set.all().order_by('-school_date'))), all_students)
        res_attendance = map(lambda x: (x[0],gen_info(x[1], num_days_old)), all_attendance)

        logging.warning(res_attendance)
        return render(request, 'home3.html', {'data': res_attendance})

@login_required
def load_locations(request):
    logging.warning(request.method)
    logging.warning(request.user)
    logging.warning(request.user.profile)
    logging.warning(request.user.profile.user_type)
    if request.method == 'POST' and request.user.profile.user_type == Profile.DRIVER_TYPE:
        driver_location = [request.user.username, request.user.profile.geo_lat, request.user.profile.geo_long, 1]
        all_students = list(User.objects.filter(profile__user_type=Profile.STUDENT_TYPE))
        all_locations = map(lambda (i, x): [x.username, x.profile.geo_lat, x.profile.geo_long, i + 2, x.profile.attendance_set.latest('school_date').going, x.profile.attendance_set.latest('school_date').picked_time is None], enumerate(all_students))
        logging.warning(all_locations) 
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
        all_studs_locations = map(lambda (i, x): [x.username, x.profile.geo_lat, x.profile.geo_long, i + 2, x.profile.attendance_set.latest('school_date').going, x.profile.attendance_set.latest('school_date').picked_time is None], enumerate(all_students))
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

@login_required
def new_day(request):
    if request.method == 'POST':
        try:
            all_students = list(Profile.objects.filter(user_type=Profile.STUDENT_TYPE))
            all_new_days = map(lambda x: Attendance(student=x), all_students)
            save_new_days = map(lambda x: x.save(), all_new_days)
            return JsonResponse({'success': True});
        except:
            return JsonResponse({'success': False});
    else:
        return JsonResponse({'success': False});

@login_required
def pick_student(request):
    if request.method == 'POST' and request.user.profile.user_type == Profile.DRIVER_TYPE:
        logging.warning(request.POST)
        data = request.POST
        if type(data) != type(dict()): # could be a QueryDict
            data = dict(data)
            for k in data: # data is (k, [V]), make it (k, V)
                data[k] = data[k][0]

        try:
            attendance = Attendance.objects.filter(student__user__username=data['student_username']).latest('school_date')
            attendance.picked_time = timezone.now()
            attendance.save()
            return JsonResponse({'success': True});
        except Exception as e:
            logging.warning(e)
            return JsonResponse({'success': False});

    else:
        return JsonResponse({'success': False});

@login_required
def not_gonna_go_to_school(request):
    if request.method == 'POST' and request.user.profile.user_type == Profile.STUDENT_TYPE:
        try:
            attendance = request.user.profile.attendance_set.latest('school_date')
            attendance.going = False
            attendance.save()
            return JsonResponse({'success': True});
        except Exception as e:
            logging.warning(e)
            return JsonResponse({'success': False});

    else:
        return JsonResponse({'success': False});

@login_required
def gonna_go_to_school(request):
    if request.method == 'POST' and request.user.profile.user_type == Profile.STUDENT_TYPE:
        try:
            attendance = request.user.profile.attendance_set.latest('school_date')
            attendance.going = True
            attendance.save()
            return JsonResponse({'success': True});
        except Exception as e:
            logging.warning(e)
            return JsonResponse({'success': False});

    else:
        return JsonResponse({'success': False});

@login_required
def alert_accident(request):
    if request.method == 'POST' and request.user.profile.user_type == Profile.DRIVER_TYPE:
        try:
            profiles = list(Profile.objects.all().exclude(user=request.user))
            notifications = map(lambda x: Notification(profile=x, notification_type=Notification.ACCIDENT_TYPE), profiles)
            # save notifications
            map(lambda x: x.save(), notifications)

            return JsonResponse({'success': True});

        except Exception as e:
            logging.warning(e)
            return JsonResponse({'success': False});

    else:
        return JsonResponse({'success': False});


def verbose_alert(alert):
    if alert.notification_type == Notification.ACCIDENT_TYPE:
        return "There was an accident on the road. Please wait for further information from the bus driver."
    elif alert.notification_type == Notification.CLOSEBY_TYPE:
        return "Bus is almost here. Please get ready for pickup."
    else:
        return "Unknown alert. Please ignore."

@login_required
def check_alert(request):
    if request.method == 'POST':
        try:
            notifications = Notification.objects.filter(profile=request.user.profile, alerted=False)
            return_data = map(lambda x: verbose_alert(x), list(notifications))
            notifications.update(alerted=True)
            return JsonResponse({'success': True, 'alerts': return_data});

        except Exception as e:
            logging.warning(e)
            return JsonResponse({'success': False});


    else:
        logging.warning('request is not POST')
        return JsonResponse({'success': False});
