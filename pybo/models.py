from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField() # DB에서 Null을 허용하지 않는 속성
    modify_date = models.DateTimeField(null=True, blank=True) # DB에서 Null을 허용하는 속성으로, 일반적으로 blank 값도 True로 설정함
    # null=True 설정 시 blank=True 설정해야 Vaildation 에러 발생하지 않음
    # blank > True : 필수 속성이 아니므로 값이 비워져있어도됨
    #       > False : 필수 속성으로 반드시 값이 채워져야함
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인 추가

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')  # 추천인 추가

class Comment_Q(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question_comment')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question_comment')  # 추천인 추가
