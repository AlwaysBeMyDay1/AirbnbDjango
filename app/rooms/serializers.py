from unittest.util import _MAX_LENGTH
from rest_framework import serializers

class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 140)