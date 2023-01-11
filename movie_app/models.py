from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from decimal import Decimal


class Director(models.Model):
    """Creating a director model"""
    name = models.CharField(max_length=255)

    @property
    def average_movie(self):
        if hasattr(self, '_average_movie'):
            return self._average_movie
        return self.movi.aggregate(Sum('director'))

    def __str__(self):
        """Overrides the '__str__' method"""
        return self.name

    class Meta:
        """Displays model name"""
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'


class Movie(models.Model):
    """Creating a movie model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    director = models.ManyToManyField(Director, blank=True, related_name='movi')
    release_date = models.DateField()
    creation_date = models.DateField(auto_now=True)
    number = models.IntegerField(default=1)  # this number field is required to count the number of films, therefore
    # This field must always contain the number one(1)

    @property
    def average_rating(self):
        """This method is needed to calculate the average rating value"""
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.review.aggregate(Avg('stars'))

    def __str__(self):
        """Overrides the '__str__' method"""
        return self.title

    class Meta:
        """Displays model name"""
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


USER_MOVIE_RATING = (
        (Decimal("1.0"), "★☆☆☆☆ (1/5)"),
        (Decimal("2.0"), "★★☆☆☆ (2/5)"),
        (Decimal("3.0"), "★★★☆☆ (3/5)"),
        (Decimal("4.0"), "★★★★☆ (4/5)"),
        (Decimal("5.0"), "★★★★★ (5/5)"),
)


class Review(models.Model):
    """Creating a review model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.DecimalField(max_digits=2, decimal_places=1, choices=USER_MOVIE_RATING, default=3.0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.movie

    class Meta:
        """Displays model name"""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
