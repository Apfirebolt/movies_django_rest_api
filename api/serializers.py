from rest_framework import serializers
from movie.models import Movie


class ListMovieSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movie
        fields = ('ID', 'Movie_Name', 'Year', 'Timing', 'Rating', 'Votes', 'Genre', 'Language',)

    def validate(self, attrs):
        if attrs.get('Movie_Name') == 'ABC':
            raise serializers.ValidationError("Movie_Name cannot be 'ABC'")
        return super().validate(attrs)
    
    def validate_Year(self, value):
        if value < 1900:
            raise serializers.ValidationError("Year cannot be less than 1900")
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)

