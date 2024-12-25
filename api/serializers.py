from rest_framework import serializers
from movie.models import Movie


class ListMovieSerializer(serializers.ModelSerializer):

    rating_star = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ('Movie_Name', 'Year', 'Timing', 'Rating', 'Votes', 'Genre', 'Language', 'rating_star')

    
    def get_rating_star(self, obj):
        if obj.Rating == '-':
            return 'No star'
        return '5 stars'
