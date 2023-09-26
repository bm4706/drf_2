from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



from rest_framework import permissions

from articles.models import Article
from articles.serializers import ArticleCreateSerializer, ArticleSerializer, ArticleListSerializer

from rest_framework.generics import get_object_or_404

class ArticleView(APIView):
    def get(self, request):
        artices = Article.objects.all()
        serializer = ArticleListSerializer(artices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # print(request.user)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

class ArticleDetailView(APIView):
    def get(self, request, article_id):
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user: # 수정은 게시글 작성만이 가능하게 해야하므로
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)
 
    
    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        pass
    
    
class CommentView(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        pass
    
    
class CommentDetailView(APIView):    
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
class LikeView(APIView):
    def post(self, request):
        pass