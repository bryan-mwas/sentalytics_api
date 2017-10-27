from rest_framework import serializers

from sentalytics.models import Polarity, Tweet


class PolaritySerializer(serializers.Serializer):
    tweets = serializers.StringRelatedField(many=True)

    class Meta:
        model = Polarity
        fields = ('name', 'tweets')


class TweetSerializer(serializers.Serializer):
    tweet_id = serializers.CharField()
    username = serializers.CharField()
    text = serializers.CharField()
    location = serializers.CharField()
    polarity = serializers.CharField()
    date = serializers.DateTimeField()

    class Meta:
        model = Tweet
        fields = ('tweet_id', 'text', 'location')
