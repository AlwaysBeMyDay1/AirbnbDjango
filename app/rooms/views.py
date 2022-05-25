from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

# api_view가 없으면 django의 view와 다를 바 없음
# django가 view를 처리하는 방식을 (drf로) 바꿔주려면 api_view 사용
@api_view(["GET", "POST"])
def rooms_view(req):
    if req.method == "GET":
        rooms = Room.objects.all()
        room_serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(room_serializer)
        # drf에서의 res는 django에서의 res와 다르다.
        # django에서의 res는 HTTP Response, drf에서의 res는 API 등 더 다양
    elif req.method == "POST":
        room_serializer = WriteRoomSerializer(data = req.data)
        if room_serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# RetrieveAPIView : 하나의 데이터만을 보고 싶을 때 사용하는 방법
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer