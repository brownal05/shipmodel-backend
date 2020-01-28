from rest_framework import serializers
from .models import Bucketlist
from .models import Vsl


class BucketlistSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

class VslSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Vsl
        fields = ('id', 'vessel', 'speedB', 'consB','speedL','consL','ifo_port','aux_steam','aux_port')
