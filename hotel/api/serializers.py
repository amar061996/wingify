from rest_framework import serializers
from rest_framework.serializers import (
	Serializer,
	ModelSerializer,
	CharField,
	IntegerField,
	DateField,
	ChoiceField,

)

from hotel.models import Room,RoomType,Properties
import datetime

#Types of Rooms
ROOM_CHOICES=(

		('single','single'),
		('double','double')
	)

#Refine Filter

REFINE_CHOICES=(

		('All','All'),
		('Weekdays','Weekdays'),
		('Weekends','Weekends'),
		('Monday','Monday'),
		('Tuesday','Tuesday'),
		('Wednesday','Wednesday'),
		('Thursday','Thursday'),
		('Friday','Friday'),
		('Saturday','Saturday'),
		('Sunday','Sunday')
	)

#Serializer for RoomType Model

class RoomTypeSerializer(ModelSerializer):

	class Meta:
		model = RoomType
		fields = ['room_type']

#Serializer for Properties Model

class PropertySerializer(ModelSerializer):
	
	class Meta:
		model  = Properties
		fields =  [
				'inventory',
				'price',
				'date'
		]		



#Serializer for Rooms Model

class RoomSerializer(ModelSerializer):
	room_type = ChoiceField(source='room_t.room_type',choices=ROOM_CHOICES)
	room_prop = PropertySerializer()
	key       = CharField(read_only=True)

	class Meta:
		model = Room
		fields = [
			'key',
			'room_type',
			'room_prop'
		]	

	def create(self,validated_data):
		
		room_type = validated_data['room_t'].get('room_type')
		room_t    = RoomType.objects.get(room_type=room_type)

		inventory = validated_data['room_prop'].get('inventory')
		price     = validated_data['room_prop'].get('price')
		date      = validated_data['room_prop'].get('date')
		
		if not (type(date).__name__=='date'):
			date = datetime.datetime.strptime(date,"%Y-%m-%d").date()

		key = room_type+'-'+str(date.strftime("%d%m%Y"))

		if not Room.objects.filter(room_t=room_t).filter(key=key).exists():

			room_prop,created = Properties.objects.get_or_create(
											inventory=inventory,
											price=price,
											date=date
										)
				
			room = Room.objects.create(room_t=room_t,room_prop=room_prop)
			room.save()
			return room

		else:
			raise serializers.ValidationError("Room Data already created for the date. To make any modifications update the value")


	
#Serializer for updating Room Properties

class RoomUpdateSerializer(ModelSerializer):
	room_prop=PropertySerializer()
	class Meta:
		model=Room
		fields=[
			'room_prop'
		]
	def update(self,instance,validated_data):
		instance.room_prop.inventory=validated_data['room_prop'].get('inventory')
		instance.room_prop.price=validated_data['room_prop'].get('price')
		instance.save()
		return instance


#Serializer for Bulk Updates

class BulkUpdateSerializer(Serializer):
	room_type=ChoiceField(choices=ROOM_CHOICES,required=True)
	from_date=DateField()
	to_date=DateField()
	inventory=IntegerField(min_value=0)
	price=IntegerField(min_value=0)
	refine=ChoiceField(choices=REFINE_CHOICES)


#Room Book Serializer

class BookRoomSerializer(Serializer):
	room_type=ChoiceField(choices=ROOM_CHOICES,required=True)
	date=DateField(required=True)
	rooms_required=IntegerField(min_value=0,required=True)