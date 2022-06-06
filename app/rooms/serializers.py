from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer()
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

    def validate(self, data):
        # 인스턴스가 있으면 -> update -> 모든 param 수정 안 할 수 있음 -> need default
        if self.instance:
            check_in = data.get('check_in', self.instance.check_in)
            check_out = data.get('check_out', self.instance.check_out)
            beds = data.get('beds', self.instance.beds)
        # 인스턴스가 없으면 -> create -> 모든 param 있음 -> no need default
        else:
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            beds = data.get('beds')
            
        if check_in == check_out:
            raise serializers.ValidationError('Not enough time between checkin-out')
        elif beds < 3:
            raise serializers.ValidationError('Your house is too small')
        
        # 위 과정에서 모두 이상없으면 data return
        # 여기서 return한 data가 create()나 update()로 전달됨
        return data
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.price = validated_data.get('price', instance.price)
        instance.beds = validated_data.get('beds', instance.beds)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.bedrooms = validated_data.get('bedrooms', instance.bedrooms)
        instance.bathrooms = validated_data.get('bathrooms', instance.bathrooms)
        instance.check_in = validated_data.get('check_in', instance.check_in)
        instance.check_out = validated_data.get('check_out', instance.check_out)
        instance.instant_book = validated_data.get('instant_book', instance.instant_book)

        instance.save()
        return instance