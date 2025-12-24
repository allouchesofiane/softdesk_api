from django.urls import path
from api.views import signup, get_current_user


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('users/me/', get_current_user, name='current_user'),
]