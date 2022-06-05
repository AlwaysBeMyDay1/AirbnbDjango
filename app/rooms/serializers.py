from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Room
        exclude = ("modified",)

class WriteRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)
    # http://127.0.0.1:8000/api/v1/rooms/?name=Dan,address=%E3%85%87%E3%85%87%E3%84%B9%E3%85%87%E3%85%81%E3%85%87,price=23,beds=2,lat=21.42,lng=23.52

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    # def validate_beds(self, beds):
    #     if beds < 5:
    #         raise serializers.ValidationError("Your house is too small")
    #     else:
    #         return beds

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        beds = data.get('beds')
        if check_in == check_out:
            raise serializers.ValidationError('Not enough time between checkin-out')
        elif beds < 3:
            raise serializers.ValidationError('Your house is too small')
        else:
            return data
            # 여기서 return한 data가 위의 create로 전달됨