from rest_framework import serializers
from .models import Room
from users.serializers import TinyUserSerializer

class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()
    class Meta :
        model = Room
        fields = ("pk", "name", "price", "instant_book", "user")


class BigRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # 표시할 field 선택하는 방법
        # 1. 표시할 field만 적어주기
        # ex. fields = ("ooo",) <제외할 필드 없으면 fields = "__all__">
        # 2. 제외할 field만 적어주기 (표시할 필드보다 제외할 필드가 더 적을 때)
        exclude = ("check_in", "check_out")