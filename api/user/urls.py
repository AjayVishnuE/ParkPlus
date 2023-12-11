from django.urls import path
from .user_views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView, Profileview,updateprofile

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('profile/', Profileview.as_view(), name="user-profile"),
    path('updateprofile/',updateprofile.as_view(),name="update-profile")

]
