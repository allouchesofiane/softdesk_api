from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    signup,
    get_current_user,
    ProjectViewSet, 
    ContributorViewSet, 
    IssueViewSet,
    CommentViewSet)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("contributors", ContributorViewSet, basename="contributors")
router.register("issues", IssueViewSet, basename="issues")
router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('users/me/', get_current_user, name='current_user'),
    path("", include(router.urls)),
]