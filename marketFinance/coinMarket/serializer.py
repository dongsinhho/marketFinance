from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" ,"email", "password"]

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","avatar", "balance","email", "create"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","avatar", "balance"]
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.balance = validated_data.get('balance', instance.balance)
        #instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

