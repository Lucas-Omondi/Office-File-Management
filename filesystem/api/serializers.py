from rest_framework import serializers
from .models import *
import os
from django.contrib.auth import get_user_model

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class CountySerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    class Meta:
        model = County
        fields = ['id', 'name', 'region']

class ConstituencySerializer(serializers.ModelSerializer):
    county = serializers.PrimaryKeyRelatedField(queryset=County.objects.all())

    class Meta:
        model = Constituency
        fields = ['id', 'name', 'county']
    def get_county(self, obj):
        return{
            "id": obj.county.id,
            "name": obj.county.name,
            "region":{
                "id": obj.county.region.id,
                "name": obj.county.region.name
            }

        }

class ProjectSerializer(serializers.ModelSerializer):
    constituency = serializers.PrimaryKeyRelatedField(queryset=Constituency.objects.all())

    class Meta:
        model = Project
        fields = "__all__"

ALLOWED_FILE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # DOCX
    "application/vnd.ms-excel",  # XLS
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX
}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".docx", ".xls", ".xlsx"}

class FileSerializer(serializers.ModelSerializer):
    project = serializers.CharField(write_only=True)  # Accepts `rfx_number` from request
    project_details = serializers.SerializerMethodField(read_only=True)  # Returns project details
    uploaded_by_name = serializers.SerializerMethodField(read_only=True)  # ✅ User first name
    formatted_size = serializers.SerializerMethodField(read_only=True)  # ✅ Readable file size
    formatted_date = serializers.SerializerMethodField(read_only=True)  # ✅ Human-readable date

    class Meta:
        model = File
        fields = [
            "id", "name", "file", "upload_date", "uploaded_by", "uploaded_by_name",
            "formatted_size", "formatted_date", "project", "project_details"
        ]
        read_only_fields = ["name"]

    def get_uploaded_by_name(self, obj):
        """✅ Get user's first name."""
        return obj.uploaded_by.first_name if obj.uploaded_by else "Unknown"

    def get_formatted_size(self, obj):
        """✅ Convert bytes to KB, MB, or GB."""
        size = obj.size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.2f} GB"

    def get_formatted_date(self, obj):
        """✅ Format date to a readable string."""
        return obj.upload_date.strftime("%B %d, %Y, %I:%M %p")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "password", "is_staff", "is_superuser", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure password is never exposed
            "is_staff": {"read_only": True},   # Prevent users from modifying this field
            "is_superuser": {"read_only": True} # Prevent direct modification
        }

    # **🔹 Create a New User with Role-Based Permissions**
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.get("role", "basic_user")  # Default to basic_user

        # **Set `is_staff` and `is_superuser` based on role**
        if role == "Super admin":
            validated_data["is_staff"] = True
            validated_data["is_superuser"] = True
        elif role == "Admin":
            validated_data["is_staff"] = True
            validated_data["is_superuser"] = False
        else:
            validated_data["is_staff"] = False
            validated_data["is_superuser"] = False

        user = User(**validated_data)

        if password:
            user.set_password(password)  # Hash the password

        user.save()
        return user

    # **🔹 Update an Existing User & Adjust Role-Based Permissions**
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.get("role", instance.role)  # Keep existing role if not provided

        # **Update `is_staff` and `is_superuser` based on new role**
        if role == "Super admin":
            instance.is_staff = True
            instance.is_superuser = True
        elif role == "Admin":
            instance.is_staff = True
            instance.is_superuser = False
        else:
            instance.is_staff = False
            instance.is_superuser = False

        # Update fields except password
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Hash the password before saving

        instance.save()
        return instance