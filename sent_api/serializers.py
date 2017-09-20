from rest_framework import serializers
# import django.db.models.fields
from sent_api.models import JumiaTweet


class JumiaTweetSerializer(serializers.Serializer):
    tweet_id = serializers.CharField(max_length=100)
    username = serializers.CharField()
    text = serializers.CharField()
    geo = serializers.CharField()
    date = serializers.DateTimeField()
