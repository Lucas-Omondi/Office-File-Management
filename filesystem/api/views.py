from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Region, County, Constituency, Project, File
from .serializers import (
    RegionSerializer, CountySerializer, ConstituencySerializer,
    ProjectSerializer, FileSerializer, UserSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsSuperAdmin, IsAdmin, IsBasicUser
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# 🔹 User Authentication Views
class RegisterView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]  # ✅ Only Super Admin can register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "access": access_token,
                "refresh": str(refresh),
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]  # Anyone can log in

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            # Generate JWT tokens (access + refresh)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),  # Long-lived token (used to get a new access token)
                "access": str(refresh.access_token),  # Short-lived token (used for authentication)
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can see their details

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)

# 🔹 Region & Location-Based Views (No Restrictions)
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can view

class CountyViewSet(viewsets.ModelViewSet):
    serializer_class = CountySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        region_id = self.kwargs.get('region_id')
        if region_id:
            return County.objects.filter(region_id=region_id)
        return County.objects.all()

class ConstituencyViewSet(viewsets.ModelViewSet):
    serializer_class = ConstituencySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        county_id = self.kwargs.get('county_id')
        if county_id:
            return Constituency.objects.filter(county_id=county_id)
        return Constituency.objects.all()

# 🔹 Project View (No restrictions applied)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = 'rfx_number'  # Use RFX number for lookup
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        constituency_id = self.kwargs.get('constituency_id')
        if constituency_id:
            return Project.objects.filter(constituency_id=constituency_id)
        return Project.objects.all()

# 🔹 File View (With Permissions)
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]  # Default permission (everyone must be logged in)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """Basic users should only see files they are allowed to access."""
        user = self.request.user
        if user.role == "basic_user":
            return File.objects.all()  # TODO: Filter files user is allowed to see
        return File.objects.all()

    def get_permissions(self):
        """Apply role-based permissions dynamically."""
        if self.action in ["list", "retrieve"]:  # Viewing/downloading files
            return [IsAuthenticated()]  # All authenticated users can view
        elif self.action in ["create", "update", "partial_update", "destroy"]:  # Upload/Edit/Delete
            return [IsAuthenticated(), IsAdmin()]  # Only admins can modify files
        return super().get_permissions()

class UserViewSet(viewsets.ModelViewSet):
    """Viewset for managing users (Admins only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]