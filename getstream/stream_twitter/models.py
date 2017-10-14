from django.contrib import auth
from django.db import models


# 3가지 model: users, tweets, and follows

class Tweet(models.Model):
    user = models.ForeignKey('auth.User')
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    # user가 follow한 다른 user들
    user = models.ForeignKey('auth.User', related_name='friends')
    # user를 follow한 다른 user들
    target = models.ForeignKey('auth.User', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')
