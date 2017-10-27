from rest_framework import serializers

from sentalytics.models import Polarity, Tweet


class PolaritySerializer(serializers.Serializer):
    name = serializers.CharField()
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
    created_date = serializers.DateField()

    class Meta:
        model = Tweet
        fields = ('tweet_id', 'text', 'location')


class MySerializer(serializers.Serializer):
    created_date = serializers.DateField()

    class Meta:
        model = Tweet
        fields = 'created_date'
