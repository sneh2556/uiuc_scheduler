"""cs411project URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from uiuc_scheduler import views

urlpatterns = [
    url(r'^view_friend_schedules/', views.view_friend_schedules, name='viewFriendSchedules'),
    url(r'^unfollow/', views.unfollow, name='unsaveSchedule'),
    url(r'^follow/', views.follow, name='unsaveSchedule'),
    url(r'^unsave_schedule/', views.unsave_schedule, name='unsaveSchedule'),
    url(r'^view_saved_schedules/', views.view_saved_schedules, name='viewSavedSchedules'),
    url(r'^save_schedule/', views.save_schedule, name='saveSchedule'),
    url(r'^view_friends/', views.view_friends, name='viewFriends'),
    url(r'^add_friend/', views.add_friend, name='addFriend'),
    url(r'^accept_request/', views.accept_request, name='acceptRequest'),
    url(r'^unfriend/', views.unfriend, name='unfriend'),
    url(r'^cancel_request/', views.cancel_request, name='cancel_request'),
    url(r'^search_people/', views.search_people, name='searchPeople'),
    url(r'^search_geneds/', views.search_geneds, name='searchGeneds'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^$', views.home_view, name='home'),
    url(r'^api/get_profs/', views.get_profs, name='get_profs'),
    url(r'^api/get_subjects/', views.get_subjects, name='get_subjects'),
    url(r'^api/get_numbers/', views.get_numbers, name='get_numbers'),
    url(r'^render_schedule/', views.render_schedule, name='render_schedule'),
    url(r'^generate_schedule/', views.generate_schedule, name='generate_schedule'),
    url(r'^generate_schedule_view/', views.generate_schedule_view, name='generate_schedule_view'),
    url(r'^generate_schedule_select_term/', views.generate_schedule_select_term_view, name='generate_select_term'),
    url(r'^search/', views.search_view, name='search'),
    url(r'^delete_rating/', views.delete_rating, name='deleteRating'),
    url(r'^update_rating/', views.update_rating, name='updateRating'),
    url(r'^insert/', views.add_rating_view, name='insert'),
    url(r'^get_prof_ratings/', views.get_prof_ratings, name='get_prof_ratings'),
    url(r'^display_prof_ratings/', views.display_prof_ratings, name='display_prof_ratings'),
    url(r'^delete_my_ratings/', views.delete_my_ratings_view, name='del_my_ratings'),
    url(r'^update_my_ratings/', views.update_my_ratings_view, name='upd_my_ratings'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^get_avg_gpa/', views.get_avg_gpa, name='gpa'),
    url(r'^admin/', admin.site.urls),
]
