from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
# Create your views here.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions

from rest_framework.generics import get_object_or_404



class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, user_id): # 회원탈퇴 기능 여기다가 넣음
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)    
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 되었을때만 가능하도록
    def get(self, request):
        print(request.user)
        user = request.user
        user.is_admin = True
        user.save()
        return Response("get 요청")

# 실험중인 회원탈퇴 기능 
# class UserDetailView(APIView):    
        
#     def delete(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)
#         if request.user == user.user:
#             user.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)    
    
# 팔로우 기능
class Followview(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all(): # 팔로우 한번더 누르면 제거기능 넣기
            you.followers.remove(me)
            return Response("팔로우를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("팔로우했습니다.", status=status.HTTP_200_OK)
        
        
# 프로필 확인!  
class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)