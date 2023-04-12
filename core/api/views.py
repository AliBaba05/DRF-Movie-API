from core.api.serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
from core.api.pagination import StandartMoviePagination, StandartDirectorPagination
from core.api.permissions import IsReviewAuthorOrReadOnly
from core.models import Movie, Director, Review

from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class MovieAPIView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = StandartMoviePagination
    
    def get_queryset(self):
        title = self.request.query_params.get('title')
        if title:
            return Movie.objects.filter(title__icontains=title)
        else:
            return Movie.objects.all()


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class DirectorAPIView(generics.ListCreateAPIView):
    serializer_class = DirectorSerializer
    pagination_class = StandartDirectorPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return Director.objects.filter(name__icontains=name)
        else:
            return Director.objects.all()
	
    
class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewAuthorOrReadOnly]

class ReviewCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        reviews = movie.reviews
        return reviews
        
    def perform_create(self, serializer):
        author = self.request.user
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])

        review = Review.objects.filter(movie=movie, author=author)

        if review.exists():
            raise ValidationError('You can only make one comment on a movie.')

        serializer.save(author=author, movie=movie)