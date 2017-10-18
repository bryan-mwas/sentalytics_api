from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sentalytics.senti_model.sentalytics import SentalyticsClassifier


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
        result = SentalyticsClassifier().classify_svm(text)
        return Response(result, status=status.HTTP_201_CREATED)
