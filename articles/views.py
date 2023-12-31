from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



from rest_framework import permissions

from articles.models import Article, Comment
from articles.serializers import ArticleCreateSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer, CommentCreateSerializer

from rest_framework.generics import get_object_or_404

from django.db.models.query_utils import Q



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
        
# 팔로우 한사람 글 보기

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인한 사람만 보도록
    def get(self, request):
        q = Q()
        for user in request.user.followings.all(): # 로그인한 유저의 팔로우한 사람의 모든것
            q.add(Q(user=user),q.OR)
        feeds = Article.objects.filter(q)
        serializer = ArticleListSerializer(feeds, many=True)
        return Response(serializer.data)









    

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
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)
 
    
    
class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        # 역참조인 set는 models.py에 따로 relatedname을 붙이지 않아도 자동으로 등록되어잇다.
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request, article_id): # 댓글 생성 기능
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id )
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentDetailView(APIView):    
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user: # 수정은 게시글 작성만이 가능하게 해야하므로
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN)
    
class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all(): # 좋아요 한번더 누르면 제거기능 넣기
            article.likes.remove(request.user)
            return Response("좋아요를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요했습니다.", status=status.HTTP_200_OK)
        