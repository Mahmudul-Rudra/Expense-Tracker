from rest_framework import serializers
from .models import ExpenseModel, Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)
    name = serializers.CharField(write_only = True)
    email = serializers.CharField(write_only = True)
    phone = serializers.CharField(write_only = True)
    gender = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password', 'name', 'email', 'phone', 'gender']
        extra_kwargs = {
            'password':{'write_only': True}
        }
        
    def validate(self, data):
        def validate(self, data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        if data['email'] and Profile.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists!"})    
        return data
    
    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        name = validated_data.pop('name')
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        gender = validated_data.pop('gender')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.profile.name = name
        user.profile.email = email
        user.profile.phone = phone
        user.profile.gender = gender
        user.profile.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'phone', 'gender']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = '__all__'
        read_only_fields = ['user']
        
