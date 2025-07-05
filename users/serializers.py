# users/serializers.py

from rest_framework import serializers
from users.models import *
from django.contrib.auth import authenticate

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'user_name', 'role', 'mobile_number', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        mobile = data.get('mobile_number')
        password = data.get('password')

        try:
            user = User.objects.get(mobile_number=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid mobile number or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid mobile number or password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data['user'] = user
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'role', 'mobile_number']

class StaffDetailsSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    user_name = serializers.CharField(source='user.user_name',read_only=True)

    class Meta:
        model = StaffDetails
        fields = [
            'user_email', 'user_role','user_name', 'alternate_mobile_number',
            'address', 'district', 'place', 'weight', 'height',
            'profile_image', 'pant', 'shoe', 'grooming', 'experienced',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'mobile_number']
        read_only_fields = ['email']

class StaffDetailsSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = StaffDetails
        exclude = ['id', 'user', 'created_at', 'updated_at']

class AdminUserListSerializer(serializers.ModelSerializer):
    staff_details = StaffDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'mobile_number', 'role', 'is_active', 'is_approved', 'staff_details']

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    staff_details = StaffDetailsSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'user_name',
            'mobile_number',
            'role',
            'is_active',
            'is_approved',
            'staff_details',
        ]

    def validate_mobile_number(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number is already in use.")
        return value

    def update(self, instance, validated_data):
        staff_data = validated_data.pop('staff_details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if staff_data and hasattr(instance, 'staff_details'):
            staff_instance = instance.staff_details
            for attr, value in staff_data.items():
                setattr(staff_instance, attr, value)
            staff_instance.save()

        return instance
