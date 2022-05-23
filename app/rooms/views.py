from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import BigRoomSerializer, RoomSerializer

# @api_view(["GET"])
# def list_rooms(request):
#     rooms = Room.objects.all()
#     serialized_rooms = RoomSerializer(rooms, many=True)
#     return Response(data=serialized_rooms.data)

# ⬇️ 동일 결과 출력 ⬆️ 
# class ListRoomsView(APIView):
#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

# ⬇️ 동일 결과 출력 ⬆️
# 많은 것을 커스터마이징할 필요가 없을 때 ListAPIView 사용
class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class SeeRoomsView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer