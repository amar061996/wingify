# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import RoomType,Properties,Room

admin.site.register(RoomType)
admin.site.register(Properties)
admin.site.register(Room)

# Register your models here.
