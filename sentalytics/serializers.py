from rest_framework import serializers

from sentalytics.models import Polarity, Tweet


class TweetSerializer(serializers.Serializer):
    tweet_id = serializers.CharField()
    username = serializers.CharField()
    text = serializers.CharField()
    location = serializers.CharField()
    polarity = serializers.CharField()
    created_date = serializers.DateField()

    class Meta:
        model = Tweet
        fields = ('tweet_id', 'text', 'location')


class PolaritySerializer(serializers.Serializer):
    name = serializers.CharField()
    tweets = TweetSerializer(many=True, read_only=True)

    class Meta:
        model = Polarity
        fields = ('name', 'tweets')