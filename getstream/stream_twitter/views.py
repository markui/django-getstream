from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from .models import Tweet, Follow

from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager

User = get_user_model()


class TweetView(CreateView):
    """
    User가 Tweet을 생성하는 CreateView

    Tweet을 생성시, 이는 api를 통해서
    Getstream.io의 Dashboard에 저장된다(Data Browser에서 확인)
    """
    # ModelForm 을 사용
    model = Tweet
    fields = ['text']

    # form.is_valid() 지난 후, form 을 save하고 success_url로 보내는 작업
    def form_valid(self, form):
        # form이 valid 할 경우
        form.instance.user = self.request.user
        # form을 save 해주기 위해
        return super(TweetView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_feed', kwargs={'username': self.request.user})


def profile_feed(request, username=None):
    """
    해당 username을 가진 user의 피드(author's feed)

    해당 user가 생성한 Tweet들을 모두 보여준다

    cf) feed manager: app과 관련된 다양한 feed들을 관리하는 데 사용
        enricher: 받아온 activity json data에서 reference를 실제 객체로 바꿔준다
    """
    enricher = Enrich()
    user = User.objects.get(username=username)
    # feed manager가 getstream 측으로부터 json data로
    # user의 feed(author's feed)를 받아온다
    feed = feed_manager.get_user_feed(user.id)
    # user feed의 activities를 dict들로 이루어진 list로 받아온다
    activities = feed.get(limit=25)['results']
    # 각 activity들의 reference를 실제 모델 인스턴스로 바꿔준다
    enricher.enrich_activities(activities)
    context = {
        'activities': activities,
    }
    return render(request, 'stream_twitter/tweets.html', context)


class FollowView(CreateView):
    model = Follow
    fields = ['target']
    success_url = '/'

    # form.is_valid() 지난 후, form 을 save하고 success_url로 보내는 작업
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def timeline(request):
    """
    유저가 팔로우하는 다른 유저의 activity들을 보여주는
    타임라인(뉴스피드) 기능
    """
    enricher = Enrich()
    feed = feed_manager.get_news_feeds(request.user.id)['timeline']
    activities = feed.get(limit=25)['results']
    enricher.enrich_activities(activities)
    context = {
        'activities': activities
    }
    return render(request, 'stream_twitter/timeline.html', context)


def hashtag(request, hashtag):
    """
    특정 해쉬태그를 포함한
    트윗들을 보여주는 기능
    """
    enricher = Enrich()
    feed = feed_manager.get_feed('hashtag', hashtag)
    activities = feed.get(limit=5)['results']
    enricher.enrich_activities(activities)
    context = {
        'activities': activities
    }
    return render(request, 'stream_twitter/hashtag.html', context)