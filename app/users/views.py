import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rooms.serializers import RoomSerializer
from users.serializers import UserSerializer
from .models import User
from rooms.models import Room

class UsersView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            new_user = user_serializer.save()
            return Response(data=UserSerializer(new_user).data)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        read_me_serializer = UserSerializer(request.user).data
        return Response(data=read_me_serializer)
    
    def get_me(self, pk):
        try:
            me = User.objects.get(pk=pk)
            return me
        except User.DoesNotExist:
            return None

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    def delete(self, request, pk):
        me = self.get_me(pk)
        if me is not None:
            if request.user == me:
                me.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        encoded_jwt = jwt.encdoe({'id':user.pk}, settings.SECRET_KEY, algorithm='HS256')
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    