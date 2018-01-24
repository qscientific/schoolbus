# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

# Create your models here.


###########################
# USER AND PROFILE

class Profile(models.Model):

    #user types
    UNKNOWN_TYPE = 'U'
    DRIVER_TYPE = 'D'
    STUDENT_TYPE = 'S'
    ADMIN_TYPE = 'A'

    USER_TYPE_OPTIONS = (
        (UNKNOWN_TYPE, 'Unknown'),
        (DRIVER_TYPE, 'Driver'),
        (STUDENT_TYPE, 'Student'),
        (ADMIN_TYPE, 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_OPTIONS, 
                                      default=UNKNOWN_TYPE)
    geo_long = models.FloatField(blank=True, null=True)
    geo_lat = models.FloatField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Attendance(models.Model):
    school_date = models.DateTimeField(auto_now_add=True)
    going = models.BooleanField(default=True)
    picked_time = models.DateTimeField(blank=True, null=True)
    closeby_alerted = models.BooleanField(default=False)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)



class Notification(models.Model):

    #notification types
    UNKNOWN_TYPE = 'U'
    CLOSEBY_TYPE = 'C'
    ACCIDENT_TYPE = 'A'

    NOTIFICATION_TYPE_OPTIONS = (
        (UNKNOWN_TYPE, 'Unknown'),
        (CLOSEBY_TYPE, 'Close By'),
        (ACCIDENT_TYPE, 'Accident'),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE_OPTIONS,
                                            default=UNKNOWN_TYPE)
    alerted = models.BooleanField(default=False)
