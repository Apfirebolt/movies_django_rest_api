from rest_framework.generics import ListAPIView
from . serializers import ListMovieSerializer
from rest_framework.response import Response
from movie.models import Movie



class ListMovieApiView(ListAPIView):
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ListMovieSerializer(queryset, many=True)
        return Response(serializer.data)

    