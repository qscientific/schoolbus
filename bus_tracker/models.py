# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

