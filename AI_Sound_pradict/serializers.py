from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from datetime import datetime

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    unique_string = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'unique_string']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Generate unique string: username+date+time
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_str = f"{user.username}_{now}"

        UserProfile.objects.create(user=user, unique_string=unique_str)
        return user


class UserLoginSerializer(serializers.Serializer):
    unique_string = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            profile = UserProfile.objects.get(unique_string=data['unique_string'])
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Invalid unique identifier")

        user = authenticate(username=profile.user.username, password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data
