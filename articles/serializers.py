from rest_framework import serializers

from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer): # 모든 정보를 볼려고함
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email
    class Meta:
        model = Article
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