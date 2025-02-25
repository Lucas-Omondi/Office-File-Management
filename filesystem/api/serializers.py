from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class CountySerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = County
        fields = ['id', 'name', 'region']

class ConstituencySerializer(serializers.ModelSerializer):
    county = CountySerializer()

    class Meta:
        model = Constituency
        fields = ['id', 'name', 'county']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['rfx_number', 'name', 'constituency', 'contracting_company', 'contract_date', 'status']

class FileSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field='rfx_number'  # Use RFX number instead of ID
    )

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'project']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', 'basic_user')  # Default to basic_user if not provided
        user = User.objects.create_user(**validated_data)

        # Assign permissions based on role
        if role == 'admin':
            user.is_staff = True  # Admin users can access Django Admin
        elif role == 'super_admin':
            user.is_staff = True
            user.is_superuser = True  # Super Admin gets full access

        user.role = role
        user.save()
        return user
