from rest_framework import status
from rest_framework.viewsets import *
from movie_app.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializers
    lookup_field = 'pk'

    @action(detail=False, methods=['post'])
    def create(self, request):
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        author = serializer.validated_data.get('author')
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director = serializer.validated_data.get('director')
        release_date = serializer.validated_data.get('release_date')
        movie = Movie.objects.create(author_id=author,
                                     title=title,
                                     description=description,
                                     duration=duration,
                                     release_date=release_date)
        movie.director.set(director)
        movie.save()
        return Response(data={'message': 'Data received!',
                              'movie': MoviesSerializers(movie).data},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update(self, request):
        movie = self.get_object()
        serializer = MovieUpdateSerializer(data=request.data,
                                           context={'id': movie.id})
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        movie.author_id = serializer.validated_data.get('author')
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.release_date = serializer.validated_data.get('release_date')
        movie.director.set(serializer.validated_data.get('director'))
        movie.save()
        return Response(data={'message': 'Data received!',
                              'movie': MoviesSerializers(movie).data},
                        status=status.HTTP_201_CREATED)


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializers
    lookup_field = 'pk'

    @action(detail=False, methods=['post'])
    def create(self, request):
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        name = serializer.validated_data.get('name')
        new_director = Director.objects.create(name=name)
        new_director.save()
        return Response(data={'message': 'Data received!',
                              'director': DirectorsSerializers(new_director).data},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update(self, request):
        director = self.get_object()
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data={'message': 'Data received!',
                              'director': DirectorsSerializers(director).data},
                        status=status.HTTP_201_CREATED)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializers
    lookup_field = 'pk'

    @action(detail=False, methods=['post'])
    def create(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        author = serializer.validated_data.get('author')
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie = serializer.validated_data.get('movie')
        review = Review.objects.create(author_id=author,
                                       text=text,
                                       stars=stars,
                                       movie_id=movie)
        review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(review).data},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update(self, request):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        review.author_id = serializer.validated_data.get('author')
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie')
        review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(review).data},
                        status=status.HTTP_201_CREATED)


class MovieReviewViewSet(MovieViewSet):
    serializer_class = MovieReviewSerializers
    lookup_field = 'pk'
