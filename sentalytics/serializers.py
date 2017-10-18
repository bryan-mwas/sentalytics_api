from rest_framework import serializers


class TweetSerializer(serializers.Serializer):
    tweet_id = serializers.CharField(max_length=100)
    username = serializers.CharField()
    text = serializers.CharField()
    geo = serializers.CharField()
    polarity = serializers.CharField()
    date = serializers.DateTimeField()
