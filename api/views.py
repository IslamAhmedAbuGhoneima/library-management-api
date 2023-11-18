from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
# Create your views here.


@api_view(['POST'])
def singup(request):
    if request.method == 'POST':
        data = request.data
        serializer = SingupSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password'])
            )
            user.save()
            return Response({
                'Message': "User Created successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'Error': "Not Valid User"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'Error': "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


def search(request, book_id):
    user = request.user
    user_books = user.user_books.all()
    # print(user_books)
    for book in user_books:
        if book.book.id == book_id:
            return True
    return False


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'price']
    ordering_fields = ['title']

    @action(methods=['GET', 'POST'], detail=True)
    def borrow_book(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except:
            return Response({
                'Error': "somthing went wrong"
            })
        if book.available > 0:
            if search(request, int(pk)):
                return Response({
                    'Error': 'You already have the book'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                book.available -= 1
                book.save()
                borrow = Borrow.objects.create(
                    user=request.user,
                    book=book,
                )
                return Response({
                    'Message': f'Member {request.user.username} borrow the book {book.title}',
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'Message': 'Sorry this book is not available now'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', 'POST'], detail=True)
    def return_book(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except:
            return Response({
                'Error': "somthing went wrong"
            })
        if search(request, int(pk)):
            book.available += 1
            book.save()
            borrow = Borrow.objects.get(
                user=request.user,
                book=book
            )
            borrow.delete()
            return Response({'Message': 'book has been returned successfully :)'})
        else:
            return Response({'Message': "You don't have such a book to return :("})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_book(request):
    query = request.GET['query'] if request.GET['query'] != None else ''
    book = Book.objects.filter(
        Q(auther__name__icontains=query) |
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular_books(request):
    books = Book.objects.all().order_by('available')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AuthersViewset(viewsets.ModelViewSet):
    queryset = Auther.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class MembersViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RatingViewset(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(methods=['POST'], detail=True)
    def rate_book(self, request, pk):
        if 'rate' in request.data:
            book = get_object_or_404(Book, id=pk)
            user = request.user
            stars = request.data['rate']
            try:
                rate = Rating.objects.get(user=user, book=book)
                rate.rate = stars
                rate.save()
                serializer = RatingSerializer(rate)
                return Response({
                    'message': 'Book Rate Updated',
                    'result': serializer.data,
                }, status=status.HTTP_200_OK)
            except:
                rate = Rating.objects.create(user=user, book=book, rate=stars)
                rate.save()
                serializer = RatingSerializer(rate)
                return Response({
                    'message': 'Book Rate Created',
                    'result': serializer.data,
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Stars not provided',
            }, status=status.HTTP_400_BAD_REQUEST)
