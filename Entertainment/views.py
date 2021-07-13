from Entertainment.serializers import MediaSerializer, FavouriteSerializer
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Media, Favourite


class AudioViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint allows user to list Audio!!
    """
    queryset = Media.objects.all().filter(Media_type='Audio')
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]


class VideoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint allows user to list Video
    """
    queryset = Media.objects.all().filter(Media_type='Video')
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]


class FavouriteAPI(viewsets.ViewSet):
    """
    Api endpoint for Favourite details
    """
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        API for get Favourite or not
        """
        user = self.request.user
        if 'Media_id' not in request.query_params:
            raise Exception('Media_id must be provided in params')
        Media_id = request.query_params.get('Media_id')
        output = FavouriteSerializer.like(self, user, Media_id), FavouriteSerializer \
            .popularity(self, Media_id)
        return Response(output)

    def create(self, request):
        """
        API for creating an Favourite
        """
        if 'Media_id' not in request.query_params:
            raise Exception('Media_id must be provided in params')
        user = self.request.user
        Media_id = request.query_params.get('Media_id')
        serializer = FavouriteSerializer(data={"user": user.id, "Media_id": Media_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('favourite created successfully', status=201)
        else:
            return Response('not a valid user', status=400)

    def destroy(self, request, pk=None):
        """
        Api for deleting Favourite
        """
        if 'Media_id' not in request.query_params:
            raise Exception('Media_id must be provided in params')
        user = self.request.user
        Media_id = request.query_params.get('Media_id')
        queryset = Favourite.objects.all().filter(user=user, Media_id=Media_id)
        if len(queryset) == 0:
            return Response('like does not exist')
        else:
            queryset.delete()
            serializer = FavouriteSerializer(queryset, many=True)
            return Response(serializer.data, status=204)
