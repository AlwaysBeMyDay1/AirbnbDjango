from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        room_serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(room_serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        room_serializer = WriteRoomSerializer(data = request.data)
        if room_serializer.is_valid():
            room = room_serializer.save(user=request.user)
            read_room_serializer = ReadRoomSerializer(room).data
            return Response(data = read_room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(data = room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RoomView(APIView):
    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass
    def delete(self, request):
        pass
