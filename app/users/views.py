import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rooms.serializers import RoomSerializer
from users.serializers import UserSerializer
from .models import User
from .permissions import IsSelf
from rooms.models import Room


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create' or self.action == 'retrieve' or self.action == 'favs':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            encoded_jwt = jwt.encode({'pk':user.pk}, settings.SECRET_KEY, algorithm='HS256')
            return Response(data={"token":encoded_jwt, "id":user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # detail=True : users/1/favs && detail=False : users/favs
    # detail=True면 항상 pk를 action의 인자로 전달, 즉 pk를 인자로 추가해야함
    @action(detail=True)
    def favs(self, request, pk):
        # request.user에는 favs에 관한 정보가 없다, get_object로 화면에 출력되는 user 정보 가져와야함.
        user = self.get_object()
        rooms = RoomSerializer(user.favs.all(), many=True, context={'request':request}).data
        return Response(rooms)
    
    # 위는 favs/ GET 메소드
    # 만약 favs/ PUT 메소드를 만들려면
    @favs.mapping.put
    def update_favs(self, request, pk):
        id = request.data.get('id', None)
        user = self.get_object()
        if id:
            try:
                room = Room.objects.get(id=id)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        # id가 없다면 error
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
