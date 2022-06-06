from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from users.serializers import ReadUserSerializer, WriteUserSerializer
from .models import User

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

    def put(self, request, pk):
        me = self.get_me(pk)
        if me is not None:
            if me == request.user:
                serializer = WriteUserSerializer(me, data=request.data, partial=True)
                if serializer.is_valid():
                    me = serializer.save()
                    read_me_serializer = ReadUserSerializer(me).data
                    return Response(data=read_me_serializer, status=status.HTTP_200_OK)
                return Response(serializer)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

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