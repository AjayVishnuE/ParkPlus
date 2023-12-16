from django.urls import path
from .user_views import RegistrationAPIView, LoginAPIView, RefreshAPIView, LogoutAPIView,updateprofile,addvehicle,Scheduleview,Ticketview

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('updateprofile/',updateprofile.as_view(),name="update-profile"),
    path('addvehicle/',addvehicle.as_view(), name="user-profile"),
    path('schedule/',Scheduleview.as_view(),name='schedule'),
    path('ticket/',Ticketview.as_view(),name='ticket')
    

]
