# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class GenEd(models.Model):
    crn = models.IntegerField(db_column='CRN', primary_key=True)  # Field name made lowercase.
    degreeattributes = models.CharField(db_column='DegreeAttributes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'gen_eds'

# #crn = models.IntegerField(db_column='CRN', primary_key=True)  # Field name made lowercase.
# subject = models.CharField(db_column='Subject', max_length=255)  # Field name made lowercase.
# number = models.IntegerField(db_column='Number')  # Field name made lowercase.
# name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
# credithours = models.CharField(db_column='CreditHours', max_length=255)  # Field name made lowercase.
# degreeattributes = models.CharField(db_column='DegreeAttributes', max_length=255, blank=True, null=True)  # Field name made lowercase.
# scheduleinfo = models.CharField(db_column='ScheduleInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
# section = models.CharField(db_column='Section', max_length=255, blank=True, null=True)  # Field name made lowercase.
# enrollmentstatus = models.CharField(db_column='EnrollmentStatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
# type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
# starttime = models.CharField(db_column='StartTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
# endtime = models.CharField(db_column='EndTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
# days = models.CharField(db_column='Days', max_length=255, blank=True, null=True)  # Field name made lowercase.
# room = models.CharField(db_column='Room', max_length=255, blank=True, null=True)  # Field name made lowercase.
# building = models.CharField(db_column='Building', max_length=255, blank=True, null=True)  # Field name made lowercase.
# instructors = models.CharField(db_column='Instructors', max_length=255, blank=True, null=True)  # Field name made lowercase.

class Gpa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    term = models.CharField(db_column='Term', max_length=255)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=255)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number')  # Field name made lowercase.
    coursetitle = models.CharField(db_column='CourseTitle', max_length=255)  # Field name made lowercase.
    avggpa = models.FloatField(db_column='avgGpa', blank=True, null=True)  # Field name made lowercase.
    a = models.IntegerField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    b = models.IntegerField(db_column='B', blank=True, null=True)  # Field name made lowercase.
    c = models.IntegerField(db_column='C', blank=True, null=True)  # Field name made lowercase.
    d = models.IntegerField(db_column='D', blank=True, null=True)  # Field name made lowercase.
    f = models.IntegerField(db_column='F', blank=True, null=True)  # Field name made lowercase.
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    primaryinstructor = models.CharField(db_column='PrimaryInstructor', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'gpa'


class RegularCourse(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    crn = models.IntegerField(db_column='CRN')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')
    term = models.CharField(db_column='Term', max_length=255)
    subject = models.CharField(db_column='Subject', max_length=255)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    credithours = models.CharField(db_column='CreditHours', max_length=255)  # Field name made lowercase.
    scheduleinfo = models.CharField(db_column='ScheduleInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enrollmentstatus = models.CharField(db_column='EnrollmentStatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    starttime = models.CharField(db_column='StartTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    endtime = models.CharField(db_column='EndTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    days = models.CharField(db_column='Days', max_length=255, blank=True, null=True)  # Field name made lowercase.
    room = models.CharField(db_column='Room', max_length=255, blank=True, null=True)  # Field name made lowercase.
    building = models.CharField(db_column='Building', max_length=255, blank=True, null=True)  # Field name made lowercase.
    instructors = models.CharField(db_column='Instructors', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'regular_courses'
        unique_together = ('crn', 'type',)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    professor_name = models.CharField(max_length=255)
    rating = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "ratings"

class friendships(models.Model):
    friendship_id = models.AutoField(db_column='friendship_id', primary_key=True)
    friend_one_id = models.ForeignKey(User, db_column='friend_one_id', on_delete=models.CASCADE, related_name='friend_one_id')
    friend_two_id = models.ForeignKey(User, db_column='friend_two_id', on_delete=models.CASCADE, related_name='friend_two_id')

    class Meta:
        db_table = "friendships"

class friendRequest(models.Model):
    request_id = models.AutoField(db_column='request_id', primary_key=True)
    sender_id = models.ForeignKey(User, db_column='sender_id', on_delete=models.CASCADE, related_name='sender_id')
    receiver_id = models.ForeignKey(User, db_column='receiver_id', on_delete=models.CASCADE, related_name='receiver_id')

    class Meta:
        db_table = "friend_requests"

class schedule(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, related_name='user_id')
    schedule_id = models.IntegerField(db_column='schedule_id')
    crn = models.IntegerField(db_column='crn')
    term = models.CharField(db_column='term', max_length=255)
    year = models.IntegerField(db_column='year')

    class Meta:
        db_table = 'schedule'

class following(models.Model):
    follow_id = models.AutoField(db_column='follow_id', primary_key=True)
    follower_id = models.ForeignKey(User, db_column='follower_id', on_delete=models.CASCADE, related_name='follower_id')
    following_id = models.ForeignKey(User, db_column='following_id', on_delete=models.CASCADE, related_name='following_id')

    class Meta:
        db_table = 'following'