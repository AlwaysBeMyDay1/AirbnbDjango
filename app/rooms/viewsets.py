from rest_framework import viewsets
from .models import Room
from .serializers import BigRoomSerializer

# ModelViewSet을 사용하면 매우매우 간편하게
# CRUD, Pagination, url 구성을 할 수 있다.
# 하지만! 논리적이지 못하다.(아무나 삭제 가능, 아무나 수정 가능)
# 좀더 논리적인 api view가 필요하면 그냥 viewset 사용하기
class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer