from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .models import Tweet
from .permissions import TweetPermission
from .serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (TweetPermission, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @detail_route(methods=['POST'])
    def retweet(self, request, *args, **kwargs):
        tweet = self.get_object()
        tweet.retweeted_by.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['POST'])
    def undo_retweet(self, request, *args, **kwargs):
        tweet = self.get_object()
        tweet.retweeted_by.remove(request.user)
        return Response(status=status.HTTP_200_OK)
