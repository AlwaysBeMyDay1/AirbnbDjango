from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer

# generic view : page 등의 정보를 갖고 있다
# generic view를 사용함으로써 별도의 설정없이 pagination 사용 가능
class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# RetrieveAPIView : 하나의 데이터만을 보고 싶을 때 사용하는 방법
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer