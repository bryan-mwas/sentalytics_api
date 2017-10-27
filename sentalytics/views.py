from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sentalytics.senti_model.sentalytics import SentalyticsClassifier
from sentalytics.models import Tweet, Polarity
from sentalytics.serializers import TweetSerializer, PolaritySerializer, MySerializer
from django.db.models import Count, Sum
import json


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


@api_view(['GET'])
def filter_tweets(request):
    if request.method == 'GET':
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)

        if month is not None:
            query_set = Tweet.objects.filter(created_date__month=month)
        elif year is not None:
            query_set = Tweet.objects.filter(created_date__year=year)
        elif month and year is not None:
            query_set = Tweet.objects.filter(created_date__year=year, created_date__month=month)
        else:
            query_set = Tweet.objects.all()

        response = TweetSerializer(query_set, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


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
        # print('I am executing AA')
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_polarity_tweets(request):
    try:
        polarity = Polarity.objects.all()
    except Tweet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PolaritySerializer(polarity, many=True)
        # print('I am executing BB')
        return Response(serializer.data, status=status.HTTP_200_OK)
