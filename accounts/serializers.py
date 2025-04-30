from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django_currentuser.middleware import (get_current_authenticated_user, get_current_user)
from accounts.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
User = get_user_model()

class RoleListSerializer(serializers.ModelSerializer):
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	class Meta:
		model = Role
		fields = '__all__'

	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by

class RoleMinimalListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = ['id', 'name']

class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = '__all__'
	
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2','first_name','last_name')
		
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        if not Role.objects.filter(user=user).exists():
            Role.objects.create(user=user, role='user')
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return data