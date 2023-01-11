from django.urls import path
from movie_app.views import *
from movie_app import views

urlpatterns = (
    path('directors/', DirectorViewSet.as_view({'get': 'list',
                                                'post': 'create'})),
    path('directors/<int:pk>/', DirectorViewSet.as_view({'get': 'retrieve',
                                                         'delete': 'destroy',
                                                         'put': 'update'})),
    path('movies/', MovieViewSet.as_view({'get': 'list',
                                          'post': 'create'})),
    path('movies/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve',
                                                   'delete': 'destroy',
                                                   'put': 'update'})),
    path('reviews/', ReviewViewSet.as_view({'get': 'list',
                                            'post': 'create'})),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve',
                                                     'delete': 'destroy',
                                                     'put': 'update'})),
    path('movies/reviews/', MovieReviewViewSet.as_view({'get': 'list'})),
    path('movies/reviews/<int:pk>/', MovieReviewViewSet.as_view({'get': 'retrieve'})),
)
