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
        elif self.action == 'create' or self.action == 'retrieve':
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

    

# my favs에는 두(세) 가지 동작이 필요
# put(add & remove) && get
class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.GET.get('user'))
        user = request.user
        # user가 가지고 있는 room 가져오기
        rooms = RoomSerializer(user.favs.all(), many=True).data
        return Response(rooms)

    def put(self, request):
        # request.data에서 id값 가져오기
        id = request.data.get('id', None)
        user = request.user
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
