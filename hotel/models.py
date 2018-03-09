# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import pre_save

from django.dispatch import receiver

import datetime
# Create your models here.

ROOM_CHOICES=(

		('single','single'),
		('double','double')
	)

class RoomType(models.Model):
	room_type=models.CharField(max_length=50,default="single",choices=ROOM_CHOICES)

	def __str__(self):
		return self.room_type

class Properties(models.Model):
	inventory=models.PositiveIntegerField(default=0)
	price=models.PositiveIntegerField()
	date=models.DateField(default=datetime.date.today)

	def __str__(self):
		return str(self.inventory)+": "+str(self.price)+": "+str(self.date.strftime("%d-%m-%Y"))

class Room(models.Model):
	
	key=models.CharField(max_length=50,primary_key=True,default=str(datetime.date.today()))
	room_t=models.ForeignKey('RoomType',on_delete=models.CASCADE)
	room_prop=models.ForeignKey('Properties',on_delete=models.CASCADE)
	

	def __str__(self):
		return self.key

#pre-save signal for SingleRoom
@receiver(pre_save,sender=Room)
def my_singleroom_callback(sender, instance, *args, **kwargs):
	instance.room_prop.save()
	if(instance.room_t.room_type=='single'):
		instance.key ="single-"+ str(instance.room_prop.date.strftime("%d%m%Y"))
	else:
		instance.key ="double-"+ str(instance.room_prop.date.strftime("%d%m%Y"))	
	


