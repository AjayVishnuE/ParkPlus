from django.urls import path
from .user_views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView, UpdateProfile, AddVehicle, \
    ScheduleView, TicketView, WalletView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('updateprofile/', UpdateProfile.as_view(), name="update-profile"),
    path('addvehicle/', AddVehicle.as_view(), name="user-profile"),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('ticket/', TicketView.as_view(), name='ticket'),
    path('wallet/', WalletView.as_view(), name='wallet'),
]
