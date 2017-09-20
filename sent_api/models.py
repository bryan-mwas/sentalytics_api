from django.db import models


# Create your models here.
class JumiaTweet(models.Model):
    tweet_id = models.CharField(max_length=100, null=True)
    username = models.TextField(null=True)
    text = models.TextField()
    geo = models.TextField(null=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ('date',)
