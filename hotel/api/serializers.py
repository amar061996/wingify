from rest_framework import serializers
from rest_framework.serializers import (
	Serializer,
	ModelSerializer,
	CharField,
	IntegerField,
	DateField,
	ChoiceField,
	MultipleChoiceField

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


class PropertyUpdateSerializer(ModelSerializer):

	inventory= IntegerField(required=False)

	price    = IntegerField(required=False)

	class Meta:
		model=Properties
		fields=[
			'inventory',
			'price'
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
	room_prop=PropertyUpdateSerializer()
	class Meta:
		model=Room
		fields=[
			'room_prop'
		]
	def update(self,instance,validated_data):

		if (validated_data['room_prop'].get('inventory')):
			new_inventory= validated_data['room_prop'].get('inventory')
		else:
			new_inventory=instance.room_prop.inventory

		if (validated_data['room_prop'].get('price')):
			new_price=validated_data['room_prop'].get('price')
		else :
			new_price=instance.room_prop.price

		new_date=instance.room_prop.date

		new_room_prop,created=Properties.objects.get_or_create(inventory=new_inventory,price=new_price,date=new_date)				
		instance.room_prop=new_room_prop
		instance.save()
		return instance


#Serializer for Bulk Updates

class BulkUpdateSerializer(Serializer):
	room_type=ChoiceField(choices=ROOM_CHOICES,required=True)
	from_date=DateField(required=False)
	to_date=DateField(required=False)
	inventory=IntegerField(min_value=0,required=False)
	price=IntegerField(min_value=0,required=False)
	refine=MultipleChoiceField(choices=REFINE_CHOICES,required=False)


#Room Book Serializer

class BookRoomSerializer(Serializer):
	room_type=ChoiceField(choices=ROOM_CHOICES,required=True)
	date=DateField(required=True)
	rooms_required=IntegerField(min_value=0,required=True)