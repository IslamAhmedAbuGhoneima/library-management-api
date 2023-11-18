from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('authers', views.AuthersViewset)
router.register('books', views.BookViewset)
router.register('members', views.MembersViewset)
router.register('rate', views.RatingViewset)

urlpatterns = [
    path('books/search/', views.search_book, name='search_book'),
    path('books/popular-books/', views.popular_books, name='popular_books'),
    path('signup/', views.singup, name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
