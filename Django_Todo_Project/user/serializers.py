from rest_framework import serializers
from .models import TodoUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoUser
        fields = ['id', 'username', 'email', 'password', 'is_login']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = TodoUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
