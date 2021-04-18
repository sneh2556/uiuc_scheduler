# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import models
from django.contrib import admin

admin.site.register(models.GenEd)
admin.site.register(models.Gpa)
admin.site.register(models.RegularCourse)
admin.site.register(models.Rating)
admin.site.register(models.friendships)
admin.site.register(models.friendRequest)

# Register your models here.
