from rest_framework.generics import (
				CreateAPIView,
				DestroyAPIView,
				ListAPIView,
				RetrieveAPIView,
				RetrieveUpdateAPIView,
				UpdateAPIView,

)

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import RoomSerializer,BulkUpdateSerializer,RoomUpdateSerializer,BookRoomSerializer

from hotel.models import Room,RoomType,Properties

import datetime

#update function 
def update_value(item,price,inventory):
	
	if price:
		item_price = price
	else: 
		item_price = item.room_prop.price
		
	if inventory:
		item_inventory = inventory
	else:
		item_inventory = item.room_prop.inventory


	item.room_prop,created = Properties.objects.get_or_create(price=item_price,inventory=item_inventory,date=item.room_prop.date)
	item.save()
	return item

#refine function

def refine(qs,refine_choice):

	refine_filter= []

	if(refine_choice == 'Weekdays'):
		refine_filter = ['Monday','Tuesday','Wednesday','Thursday','Friday']

	elif(refine_choice == 'Weekends'):
		refine_filter = ['Saturday','Sunday']

	else: refine_filter = [refine_choice]

	refined_qs = [item for item in qs if item.room_prop.date.strftime('%A') in refine_filter]

	return refined_qs		
#Class Based Views for SingleRoom Class

class RoomListView(ListAPIView):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

class RoomCreateView(CreateAPIView):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer	


class RoomUpdateViewSet(ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

	def get_serializer_class(self):
		serializer_class = self.serializer_class

		if self.request.method == 'PUT':
			serializer_class = RoomUpdateSerializer

		return serializer_class


class BulkUpdateView(APIView):
	serializer_class = BulkUpdateSerializer

	def put(self,request):

		room_t    	  = RoomType.objects.get(room_type=request.data['room_type'])
		from_date 	  = request.data['from_date']	
		to_date   	  = request.data['to_date']
		price     	  = request.data['price']	
		inventory 	  = request.data['inventory']
		refine_choice = request.data['refine']

	
		prop_qs = Properties.objects.filter(date__range=[from_date,to_date])
		qs = Room.objects.filter(room_t=room_t).filter(room_prop__in=prop_qs)
		
		if refine_choice and refine_choice!='All': 

			refined_qs = refine(qs,refine_choice)         #filter queryset based on refine filter

		else:
			refined_qs=qs

		result_qs=[update_value(item,price,inventory) for item in refined_qs]  #update the values of the selected queryset
		
		if len(result_qs)>0:
			return Response(RoomSerializer(result_qs,many=True).data,status=status.HTTP_200_OK)

		else: 
			return Response({'Error':'Data could not be updated. Please check parameters'},status=status.HTTP_400_BAD_REQUEST)



class BookRoomView(APIView):
	serializer_class=BookRoomSerializer

	def post(self,request):

		room_t    = RoomType.objects.get(room_type=request.data['room_type'])
		date 	  = request.data['date']	
		rooms_req = int(request.data['rooms_required'])

		date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
		key  = room_t.room_type+'-'+str(date.strftime("%d%m%Y"))

		if Room.objects.filter(key=key).exists():
			room = Room.objects.get(key=key)

			if(room.room_prop.inventory>=rooms_req):
				inventory_left = room.room_prop.inventory-rooms_req
				new_room_prop,created=Properties.objects.get_or_create(inventory = inventory_left,price=room.room_prop.price,date=room.room_prop.date)
				room.room_prop=new_room_prop
				room.save()

				total = room.room_prop.price*rooms_req

				return Response({'Accepted':'Rooms Booked. Total Amount: '+str(total)},status = status.HTTP_202_ACCEPTED)

			else:
				return Response({'Error':'Insufficient Rooms'},status = status.HTTP_406_NOT_ACCEPTABLE)

		else: return Response({'Error':'Room not available on the specified date'},status = status.HTTP_406_NOT_ACCEPTABLE)


