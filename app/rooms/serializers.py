from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    is_fav = serializers.SerializerMethodField()
    # get_is_fav가 싫다면, method_name=""설정 가능

    class Meta:
        model = Room
        exclude = ("modified", )
        read_only_fields = ["user", "id", "created", "updated"]
    
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

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return True
        