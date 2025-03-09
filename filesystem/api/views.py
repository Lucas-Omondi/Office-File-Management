from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Region, County, Constituency, Project, File
from .serializers import (
    RegionSerializer, CountySerializer, ConstituencySerializer,
    ProjectSerializer, FileSerializer, UserSerializer
)
from .permissions import IsSuperAdmin, IsAdmin

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


# ✅ Project ViewSet (Uses RFX Number)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        constituency_id = self.kwargs.get("constituency_id")
        return Project.objects.filter(constituency_id=constituency_id) if constituency_id else Project.objects.all()

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
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
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        if user.role == "basic_user":
            return File.objects.all()  # TODO: Filter files user is allowed to see
        return File.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # Viewing files
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:  # Upload/Edit/Delete
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()


# ✅ User Management ViewSet (Admins Only)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

