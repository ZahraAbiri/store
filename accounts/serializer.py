from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
