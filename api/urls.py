from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    signup,
    get_current_user,
    ProjectViewSet, ContributorViewSet)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("contributors", ContributorViewSet, basename="contributors")


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('users/me/', get_current_user, name='current_user'),
    path("", include(router.urls)),
]