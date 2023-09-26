from rest_framework import serializers
from users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleListSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    followers =serializers.StringRelatedField(many=True) # 이러면 email로 누가 팔로우했는지 보여줌
    # followers =serializers.PrimaryKeyRelatedField(many=True, read_only=True) # 이거는 email이 아니라 userid를 보여줌
    followings =serializers.StringRelatedField(many=True)
    article_set = ArticleListSerializer(many=True)
    like_articles = ArticleListSerializer(many=True)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("id","email","followings", "followers", "article_set", "like_articles")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data):
        user =  super().create(validated_data)
        password = user.password
        user.set_password(password) # 비밀번호 해싱
        user.save() # db에 저장
        return user
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password) 
        user.save() 
        return user
    
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        

        return token