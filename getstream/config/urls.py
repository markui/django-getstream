"""getstream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from stream_twitter import views
from stream_twitter.views import profile_feed, FollowView, timeline, hashtag, notification

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tweet/$', login_required(views.TweetView.as_view(), login_url='/login/'), name='tweet'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^(?P<username>\w+)/feed/$', profile_feed, name='profile_feed'),
    url(r'^follow/$', FollowView.as_view(), name='follow'),
    url(r'^timeline/$', timeline, name='timeline'),
    url(r'^notification/$', notification, name='notification'),
    url(r'^(?P<hashtag>\w+)/hashtag/$', hashtag, name='hashtag')
]
