from django.db import models


# Create your models here.
class Polarity(models.Model):
    name = models.CharField(max_length=5)


class Tweet(models.Model):
    tweet_id = models.AutoField(max_length=100, primary_key=True)
    username = models.TextField(null=True)
    text = models.TextField()
    location = models.TextField(null=True)
    polarity = models.ForeignKey(Polarity, null=True, related_name='tweets', on_delete=models.CASCADE,)
    created_date = models.DateField()

    class Meta:
        ordering = ('created_date',)

