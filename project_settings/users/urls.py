from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from .views import UserCreateView,Logout




urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='Login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),       
    path('register/', UserCreateView.as_view(), name='Register'),
    path('logout/',Logout.as_view(),name='logout')
]





