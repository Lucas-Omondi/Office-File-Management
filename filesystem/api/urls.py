from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register(r'regions', RegionViewSet)
router.register(r'counties', CountyViewSet, basename='county')
router.register(r'constituencies', ConstituencyViewSet, basename='constituency')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'files', FileViewSet, basename='file')



urlpatterns = [
    path('', include(router.urls)),

    # ✅ Add the summary stats endpoint
    path("summary/stats/", SummaryViewSet.as_view(), name="summary-stats"),

    # Authentication & User-related endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path("users/me/", CurrentUserView.as_view(), name="current-user"),


    # Project-specific files
    # path('projects/<str:rfx_number>/files/', FileViewSet.as_view({'get': 'list'}), name='project-files'),
]
