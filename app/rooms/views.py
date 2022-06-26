from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import RoomSerializer


class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        # request를 parsing한다는 건 paginator가 page query argument를 찾아내야 한다는 뜻
        room_serializer = RoomSerializer(results, many=True).data
        return paginator.get_paginated_response(room_serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        room_serializer = RoomSerializer(data = request.data)
        print(room_serializer)
        if room_serializer.is_valid():
            room = room_serializer.save(user=request.user)
            read_room_serializer = RoomSerializer(room).data
            return Response(data = read_room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(data = room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                read_room_serializer = RoomSerializer(room).data
                return Response(read_room_serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # if, 'room'이라는 instance가 없다면 drf는 이를 create로 인식
            # 즉, instance를 통해 Write 메소드의 종류(create, put, push,,)를 결정
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        # first, get room
        room = self.get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # second, owner validate
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else :
            room.delete()
            return Response(status=status.HTTP_200_OK)

@api_view(['GET'])     
def room_search(request):
    paginator = OwnPagination()
    rooms = Room.objects.filter()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True).data
    return paginator.get_paginated_response(serializer)