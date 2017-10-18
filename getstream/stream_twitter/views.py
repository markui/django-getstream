from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from stream_twitter.models import Tweet, Follow

from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager

User = get_user_model()


# Tweet을 생성하는 CreateView
class TweetView(CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TweetView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_feed', kwargs={'username': self.request.user})


# 해당 username을 가진 user의 피드
# 해당 user가 생성한 Tweet들을 모두 보여줌
def profile_feed(request, username=None):
    enricher = Enrich()
    user = User.objects.get(username=username)
    feed = feed_manager.get_user_feed(user.id)
    activities = feed.get(limit=25)['results']
    enricher.enrich_activities(activities)
    context = {
        'activities': activities,
    }
    return render(request, 'stream_twitter/tweets.html', context)
