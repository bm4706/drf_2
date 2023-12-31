from django.db import models

from users.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True) # 생성할때만 갱신
    updated_at = models.DateTimeField(auto_now=True) # 세이브할때마다 갱신
    likes = models.ManyToManyField(User, related_name="like_articles") # 좋아요 기능! 은 many를 써야하고 related도 써야한다
    
    def __str__(self):
        return str(self.title)
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE) 
    # 글이 삭제되면 글에 작성된 댓글도 사라지게 해야하므로 추가
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)