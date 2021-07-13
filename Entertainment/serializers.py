from rest_framework import serializers
from .models import Media, Favourite


class MediaSerializer(serializers.ModelSerializer):
    like_by_user = serializers.SerializerMethodField('get_like')
    popularity = serializers.SerializerMethodField('get_popularity')

    class Meta:
        model = Media
        fields = ['Media_id', 'Media_link', 'Media_type', 'Title',
                  'Description', 'Thumbnail', 'created_on', 'like_by_user', 'popularity']

    def get_like(self, obj):
        user = self.context['request'].user
        Media_id = obj.Media_id
        return FavouriteSerializer.like(self, user, Media_id)

    def get_popularity(self, obj):
        Media_id = obj.Media_id
        return FavouriteSerializer.popularity(self, Media_id)


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['user', 'Media_id']

    def popularity(self, Media_id):
        """
        for get number of likes for media
        """
        return Favourite.objects.all().filter(Media_id=Media_id).count()

    def like(self, user, Media_id):
        """
        This is for get liked or not for media
        """
        queryset = Favourite.objects.all().filter(user=user, Media_id=Media_id)
        if len(queryset) == 0:
            return False
        if len(queryset) == 1:
            return True
        else:
            return "Something went wrong in database"
