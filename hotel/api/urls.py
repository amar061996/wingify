from django.conf.urls import url

from .views import (
	RoomListView,
	RoomCreateView,
	RoomUpdateViewSet,
	BulkUpdateView,
	BookRoomView

	)

urlpatterns=[
	
	#urls for SingleRoom Class

	url(r'^rooms/$',RoomListView.as_view(),name='room-list'),
	url(r'^rooms/create/$',RoomCreateView.as_view(),name='room-create'),
	url(r'^rooms/book/$',BookRoomView.as_view(),name='room-book'),
	url(r'^rooms/update/(?P<pk>single-\d{2}\d{2}\d{4})/$',RoomUpdateViewSet.as_view({'get': 'retrieve', 'put':'update'}),name='single-room-update'),
	url(r'^rooms/update/(?P<pk>double-\d{2}\d{2}\d{4})/$',RoomUpdateViewSet.as_view({'get': 'retrieve', 'put':'update'}),name='double-room-update'),
	url(r'^bulk-update/$',BulkUpdateView.as_view(),name='bulk-update'),
]