from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# 회원가입기능
from users import views



urlpatterns = [
    path('signup/', views.UserView.as_view(),name="user_view"),# 회원가입
    path('signup/<int:user_id>/', views.UserView.as_view(),name="user_delete"), # 회원 탈퇴기능
    path('mock/', views.mockView.as_view(),name="mock_view"),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', views.Followview.as_view(), name='follow_view'),
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
]