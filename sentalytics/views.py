from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sentalytics.senti_model.sentalytics import SentalyticsClassifier
from sentalytics.models import Tweet
from sentalytics.serializers import TweetSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def get_sentiment(request):
    """
    Triggers the model to start classification
    :param request:
    :return:
    """
    if request.method == 'POST':
        text = request.data['text']
        result = int(SentalyticsClassifier().classify_text(text))  # the result corresponds to the id in polarity table
        return Response(result, status=status.HTTP_201_CREATED)


def get_batch_sentiments(request):
    """
    Classifies a range of tweets based on the date a user selects
    :param request:
    :return:
    """
    pass


def time_lines():
    pass


@api_view(['GET'])
def get_tweets(request):
    """
       Retrieve, update or delete a code snippet.
       """
    try:
        tweet = Tweet.objects.all()
    except Tweet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TweetSerializer(tweet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # tweets = Tweet.objects.all()
        # return Response(tweets, status=status.HTTP_200_OK)
