from django.conf import settings
from django.db import models


class Tweet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tweets'
    )
    body = models.CharField(max_length=140)
    retweeted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='retweets',
        blank=True
    )

    def __str__(self):
        return 'Tweet {}'.format(self.id)
