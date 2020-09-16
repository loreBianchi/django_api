from rest_framework import serializers
from .models import Songs



class SongsSerializer(serializers.ModelSerializer):
    is_awesome = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = Songs
        fields = ('title', 'artist', 'is_awesome')

