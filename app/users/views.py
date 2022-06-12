from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rooms.serializers import RoomSerializer
from users.serializers import ReadUserSerializer, WriteUserSerializer
from .models import User
from rooms.models import Room

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        read_me_serializer = ReadUserSerializer(request.user).data
        return Response(data=read_me_serializer)
    
    def get_me(self, pk):
        try:
            me = User.objects.get(pk=pk)
            return me
        except User.DoesNotExist:
            return None

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
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

@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
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


        