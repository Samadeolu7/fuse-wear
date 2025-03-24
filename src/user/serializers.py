from rest_framework import serializers
from .models import ACTION_CHOICES, CustomUser, UserActivity

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'profile_image_url', 'preferences', 'password', 'confirm_password')
        read_only_fields = ('id',)

    def validate(self, data):
        # Check if both password and confirm_password are provided
        password = data.get('password')
        confirm_password = data.get('confirm_password')
    
        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserActivitySerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=ACTION_CHOICES)

    class Meta:
        model = UserActivity
        fields = ('id', 'user', 'action', 'timestamp', 'ip_address', 'meta_data')
        read_only_fields = ('id', 'timestamp')