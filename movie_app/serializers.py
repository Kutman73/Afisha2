from django.db.models import Avg, Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie_app.models import *


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        # The 'fields' variable holds the model fields for display
        fields = '__all__'


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # The 'fields' variable holds the model fields for display
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        # The 'fields' variable holds the model fields for display
        exclude = 'movie'.split()


class DirectorsSerializers(serializers.ModelSerializer):
    mov = MovieSerializers

    class Meta:
        model = Director
        # The 'fields' variable holds the model fields for display
        fields = ('id', 'name', 'movie_count')

    movie_count = serializers.SerializerMethodField()

    def get_movie_count(self, ob):
        # reverse lookup on Movies using item field
        return ob.movi.all().aggregate(Sum('number'))['number__sum']


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, name):
        if Director.objects.filter(name=name).count() > 0:
            raise ValidationError('Name producer must be unique!')
        return name


class MoviesSerializers(serializers.ModelSerializer):
    # review = ReviewSerializers(many=True)

    class Meta:
        model = Movie
        # The 'fields' variable holds the model fields for display
        fields = ('id', 'author', 'title', 'description', 'duration',
                  'director', 'release_date', 'creation_date')


class MovieValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=700)
    duration = serializers.DurationField()
    director = serializers.ListField(allow_empty=False, min_length=1, child=serializers.IntegerField(min_value=1))
    release_date = serializers.DateField()

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_director(self, director):
        filtered_directors = Director.objects.filter(id__in=director)
        if len(filtered_directors) != len(director):
            raise ValidationError('Director not found!')
        return director


class MovieCreateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title=title).count() > 0:
            raise ValidationError('Title must be unique')
        return title


class MovieUpdateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title=title).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title


class ReviewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        # The 'fields' variable holds the model fields for display
        fields = ('id', 'author', 'text', 'movie', 'creation_date', 'stars')

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class ReviewValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    text = serializers.CharField(max_length=500)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie = serializers.IntegerField(min_value=1)

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_movie(self, movie):
        try:
            Movie.objects.get(id=movie)
        except Movie.DoesNotExist:
            raise ValidationError('Movie not found!')
        return movie


class MovieReviewSerializers(MoviesSerializers):
    review = ReviewSerializers(many=True)

    class Meta:
        model = Movie
        # The 'fields' variable holds the model fields for display
        fields = ('id', 'author', 'title', 'description', 'duration',
                  'director', 'rating', 'release_date', 'creation_date', 'review',)

    rating = serializers.SerializerMethodField()

    def get_rating(self, ob):
        # reverse lookup on Reviews using item field
        return ob.review.all().aggregate(Avg('stars'))['stars__avg']
