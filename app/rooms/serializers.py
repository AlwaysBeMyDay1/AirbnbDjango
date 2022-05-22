from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta :
        model = Room
        fields = ("name", "price", "instant_book")
