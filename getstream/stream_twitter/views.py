from django.shortcuts import render
from stream_twitter.models import Tweet
from stream_twitter.models import Follow

from django.views.generic.edit import CreateView

class TweetView(CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TweetView, self).form_valid(form)





