from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'superhost')
        read_only_fields = ['id', 'avatar', 'superhost']

    def validate_last_name(self, value):
        return value.upper()
    # ⬇️ 아래처럼은 개별 데이터 수정이 안 되는 것으로 파악됨
    # def validate(self, data):
    #     data.last_name = data.last_name.upper()
    #     return data

    def create(self, validated_data):
        password = validated_data.get('password')
        new_user = super().create(validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user
