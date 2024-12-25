from rest_framework import serializers
from movie.models import Movie


class ListMovieSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movie
        fields = ('ID', 'Movie_Name', 'Year', 'Timing', 'Rating', 'Votes', 'Genre', 'Language',)

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)

