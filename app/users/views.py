from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import ReadMeSerializer
from .models import User

class MeView(APIView):
    def get_me(self, pk):
        try:
            me = User.objects.get(pk=pk)
            return me
        except User.DoesNotExist:
            return None

    def get(self, request):
        pk = request.user.id
        me = self.get_me(pk)
        if me is not None:
            serializer = ReadMeSerializer(me).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        me = self.get_me(pk)
        if me is not None:
            if me == request.user:
                serializer = WriteMeSerializer(me, data=request.data, partial=True)
                if serializer.is_valid():
                    me = serializer.save()
                    read_me_serializer = ReadMeSerializer(me).data
                    return Response(status=status.HTTP_200_OK)
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
