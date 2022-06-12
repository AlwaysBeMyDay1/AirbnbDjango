from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "favs",
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'superhost')
        read_only_fields = ['id', 'avatar', 'superhost']

    def validate_last_name(self, value):
        print(value)
        return value.upper()
    # ⬇️ 아래처럼은 데이터 수정이 안 되는 것으로 파악됨
    # def validate(self, data):
    #     data.last_name = data.last_name.upper()
    #     return data