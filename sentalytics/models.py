from django.db import models


# Create your models here.
class Tweet(models.Model):
    tweet_id = models.AutoField(max_length=100, primary_key=True)
    username = models.TextField(null=True)
    text = models.TextField()
    location = models.TextField(null=True)
    polarity = models.CharField(max_length=50, null=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ('date',)
