from django.contrib import auth
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from stream_django import activity
from stream_django.feed_manager import feed_manager


# 3가지 model: users, tweets, and follows

class Tweet(activity.Activity, models.Model):
    user = models.ForeignKey('auth.User', related_name='tweets')
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    # hashtag(#) 있는 tweet 단어들 parsing 하기
    def parse_hashtags(self):
        return [slugify(i) for i in self.text.split() if i.startswith('#')]

    # 필수!: activity의 object 목적어 정의
    @property
    def activity_object_attr(self):
        return self

    # sends a copy of an activity to many feeds(target feed)
    @property
    def activity_notify(self):
        # 해당 hashtag 키워드의 피드(e.g. hashtag:패션)
        #
        target_feed = []
        for hashtag in self.parse_hashtags():
            target_feed.append(feed_manager.get_feed('hashtag', hashtag))
        return target_feed


class Follow(models.Model):
    # user가 follow한 다른 user들
    user = models.ForeignKey('auth.User', related_name='following')
    # user를 follow한 다른 user들
    target = models.ForeignKey('auth.User', related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')


def follow_feed(sender, instance, created, **kwargs):
    if created:
        feed_manager.follow_user(instance.user_id, instance.target_id)


def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)


# 팔로우를 하는 순간, 팔로우하는 유저의 getstream feed가
# 타겟 유저의 피드를 팔로우함
post_save.connect(follow_feed, sender=Follow)

# 팔로우를 취소하는 순간, 팔로우하는 유저의 getstream feed가
# 타겟 유저의 피드를 언팔로우함
post_delete.connect(unfollow_feed, sender=Follow)
