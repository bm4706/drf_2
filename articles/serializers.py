from rest_framework import serializers

from articles.models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer): # 모든 정보를 볼려고함
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email
    class Meta:
        model = Article
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"
        
        
class ArticleListSerializer(serializers.ModelSerializer): # 필요한 정보만 볼려고함
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email # 이러면 이제 user값이 email로 변경되어서 보여줌
    class Meta:
        model = Article
        fields = ("id","title","image","updated_at","user")
        
        
class ArticleCreateSerializer(serializers.ModelSerializer): # 게시글 작성 하는것도 따로 해줘야함
    class Meta:
        model = Article
        fields = ("title","content","image")
        
        
class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ("content",) # fiels의 경우 하나만 넣고싶더라도 마지막에 ,를 넣어야 에러가 안뜸