from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django_currentuser.middleware import (get_current_authenticated_user, get_current_user)
from accounts.models import *
from rest_framework import serializers
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


class UserListSerializer(serializers.ModelSerializer):
	role = serializers.SerializerMethodField()
	created_by = serializers.SerializerMethodField()
	updated_by = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		exclude = ['password']
	
	def get_role(self, obj):
		return obj.role.name if obj.role else obj.role

	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by
	
class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'

		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
		}

	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])
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