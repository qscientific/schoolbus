"""qsc_school_bus_tracker_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from bus_tracker import views as bus_tracker_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', bus_tracker_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^home/$', bus_tracker_views.home, name='home'),
    url(r'^load_locations/$', bus_tracker_views.load_locations, name='load_locations'),
    url(r'^update_locations/$', bus_tracker_views.update_locations, name='update_locations'),
    url(r'^new_day/$', bus_tracker_views.new_day, name='new_day'),
    url(r'^not_gonna_go_to_school/$', bus_tracker_views.not_gonna_go_to_school, name='not_gonna_go_to_school'),
    url(r'^gonna_go_to_school/$', bus_tracker_views.gonna_go_to_school, name='gonna_go_to_school'),
    url(r'^pick_student/$', bus_tracker_views.pick_student, name='pick_student'),
    url(r'^alert_accident/$', bus_tracker_views.alert_accident, name='alert_accident'),
    url(r'^check_alert/$', bus_tracker_views.check_alert, name='check_alert'),
    url(r'^closeby_student/$', bus_tracker_views.closeby_student, name='closeby_student'),
    url(r'^delete_students/$', bus_tracker_views.delete_students, name='delete_students'),


    #index page
    url(r'^', bus_tracker_views.index, name='index'),
]
