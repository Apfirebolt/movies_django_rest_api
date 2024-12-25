from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . serializers import ListMovieSerializer
from rest_framework.response import Response
from movie.models import Movie



class ListMovieApiView(ListCreateAPIView):
    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ListMovieSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = ListMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class DetailMovieApiView(RetrieveUpdateDestroyAPIView):

    serializer_class = ListMovieSerializer
    queryset = Movie.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListMovieSerializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ListMovieSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    