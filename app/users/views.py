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
class FavsView(APIView, id):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.GET.get('user'))
        user = request.user
        # user가 가지고 있는 room 가져오기
        rooms = RoomSerializer(user.favs.all(), many=True).data
        return Response(rooms)

    def put(self, request, id):
        print(id)
        # id를 가지는 room을 찾고
        room = Room.objects.get(pk=id)
        user = request.user
        if room:
            # room이 있다면 favs에 해당 id 룸이 있는지 확인하고
            fav = user.favs.get(id=id)
            # 없으면 favs에 add
            if fav :
                user.favs.add(room)
            # 있으면 favs로부터 remove
            else :
                user.favs.remove(room)
            return Response()
        # room이 없다면 error
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


        