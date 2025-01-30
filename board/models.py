from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    regdate = models.DateTimeField(auto_now=timezone.now)
    readcount = models.IntegerField(default=0)
    
    def __str__(self):
        return '%s. %s(%d)'%(self.title,self.writer,self.readcount)
    def incrementReadCount(self):
        self.readcount+=1
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # 댓글 내용의 처음 50자 출력