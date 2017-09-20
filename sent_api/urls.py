from django.conf.urls import url
from sent_api import views

urlpatterns = [
    url(r'^tweets/$', views.tweet_list),
    url(r'^tweets/(?P<pk>[0-9]+)/$', views.tweet_detail),
]