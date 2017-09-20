from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from sent_api.models import JumiaTweet
from sent_api.serializers import JumiaTweetSerializer

# Create your views here.
@csrf_exempt
def tweet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        tweets = JumiaTweet.objects.all()
        serializer = JumiaTweetSerializer(tweets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = JumiaTweetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tweet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = JumiaTweet.objects.get(pk=pk)
    except JumiaTweet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = JumiaTweetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JumiaTweetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
