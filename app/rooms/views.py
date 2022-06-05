from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

# api_view가 없으면 django의 view와 다를 바 없음
# django가 view를 처리하는 방식을 (drf로) 바꿔주려면 api_view 사용
@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        room_serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(room_serializer)
        # drf에서의 res는 django에서의 res와 다르다.
        # django에서의 res는 HTTP Response, drf에서의 res는 API 등 더 다양
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        room_serializer = WriteRoomSerializer(data = request.data)
        # dir(room_serializer)을 통해 시리얼라이저 내부를 볼 수 있음.
        # 이를 실행하면 커스터마이징 할 수 있는 메소드들이 보이는데,
        # 그 메소드들은 serializers.py에서 커스터마이징 할 수 있다.
        if room_serializer.is_valid():
            # room_serializer.create()라고 치지 않아도 save method가 우리가 뭘 원하는지(create, save, update 중에서) 찾아냄.
            # in drf doc, it said 'Calling save() will either create a new instance, or update an existing instance,
            # depending on if an existing instance was passed when instanting the serializer class
            room = room_serializer.save(user=request.user)
            # 생성된 room instance를 room 변수에 저장하고 이를 Read형태로 바꿔서
            read_room_serializer = ReadRoomSerializer(room).data
            # Response에 전달하면 응답창에서 Read 가능
            return Response(data = read_room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# RetrieveAPIView : 하나의 데이터만을 보고 싶을 때 사용하는 방법
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer