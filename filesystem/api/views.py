from mypyc.doc.conf import project
from rest_framework import viewsets, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions, SAFE_METHODS
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Region, County, Constituency, Project, File
from .serializers import (
    RegionSerializer, CountySerializer, ConstituencySerializer,
    ProjectSerializer, FileSerializer, UserSerializer
)
from .permissions import IsSuperAdmin, IsAdmin, IsAdminOrSuperAdmin
from rest_framework.permissions import BasePermission
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404


User = get_user_model()

# ✅ Generate JWT tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

# ✅ Register View (Only Super Admins can register new users)
class RegisterView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Login View (Generates JWT tokens)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # 🔹 Ensure both username and password are provided
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            tokens = get_tokens_for_user(user)
            return Response({
                "refresh": tokens["refresh"],
                "access": tokens["access"],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ Get Current User Details
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Current User:", request.user)  # Debugging
        print("User Authenticated:", request.user.is_authenticated)
        return Response(UserSerializer(request.user).data)


# ✅ Region ViewSet (Only Authenticated Users)
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]


# ✅ County ViewSet (Filtered by Region)
class CountyViewSet(viewsets.ModelViewSet):
    serializer_class = CountySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        region_id = self.kwargs.get("region_id")
        return County.objects.filter(region_id=region_id) if region_id else County.objects.all()


# ✅ Constituency ViewSet (Filtered by County)
class ConstituencyViewSet(viewsets.ModelViewSet):
    serializer_class = ConstituencySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        county_id = self.kwargs.get("county_id")
        return Constituency.objects.filter(county_id=county_id) if county_id else Constituency.objects.all()

class AdminOnlyDeletePermission(BasePermission):
    def has_permission(self, request, view):

        """ Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_staff  # Only Admins & Super Admins can modify

    def has_object_permission(self, request, view, obj):
        """ Ensure only Admins or Super Admins can delete a project """
        if request.method == "DELETE":
            return request.user.is_superuser or request.user.is_staff
        return True  # Allow other permitted actions
# ✅ Project ViewSet (Uses ID)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "id"
    permission_classes = [IsSuperAdmin, IsAuthenticated, IsAdmin]

    def get_queryset(self):
        constituency_id = self.kwargs.get("constituency_id")
        return Project.objects.filter(constituency_id=constituency_id) if constituency_id else Project.objects.all()

    def get_permissions(self):
        print(f"DEBUG: get_permissions() called for action: {self.action}")  # 🔍 Check which action is being called

        if self.action in ["list", "retrieve"]:  # ✅ All authenticated users should be able to view
            print("DEBUG: View permissions applied (IsAuthenticated)")
            return [permissions.IsAuthenticated()]

        elif self.action in ["create", "update", "partial_update"]:  # ✅ Only Admins & Super Admins can modify
            print("DEBUG: Modify permissions applied (IsAdmin or IsSuperAdmin)")
            return [IsAdminOrSuperAdmin()]

        elif self.action == "destroy":  # ✅ Strict delete permission
            print("DEBUG: Delete permissions applied (IsSuperAdmin only)")
            return [IsSuperAdmin()]

        return super().get_permissions()

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated, AdminOnlyDeletePermission])
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({"error": "No project IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Project.objects.filter(id__in=ids).delete()
        print(f"Deleted {deleted_count} projects.")
        return Response(
            {"message": f"{deleted_count} projects deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

# ✅ File ViewSet (With Role-Based Permissions)
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter files by project (rfx_number).
        """
        queryset = File.objects.all()
        project_rfx = self.request.query_params.get("project")

        if project_rfx:
            queryset = queryset.filter(project__rfx_number=project_rfx)

        return queryset
    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        file_instance = get_object_or_404(File, id=pk)
        file_path = file_instance.file.path  # Adjust based on your model field

        try:
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_instance.name)
        except FileNotFoundError:
            raise Http404("File not found")

# ✅ User Management ViewSet (Admins Only)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def toggle_active(self, request, pk=None):
        """
        Toggle the active status of a user.
        """
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"message": "User status updated", "is_active": user.is_active})

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class SummaryViewSet(APIView):
    permission_classes = [IsAuthenticated]  # Optional: Require authentication

    def get(self, request):
        return Response({
            "projects": Project.objects.count(),
            "users": User.objects.count(),
            "constituencies": Constituency.objects.count(),
            "files": File.objects.count(),
        })