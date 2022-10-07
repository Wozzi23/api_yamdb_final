import uuid

from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilters
from .paginations import CommentsPaginator
from .permissions import AdminOnly, AdminOrReadOnly, IsAdminOrAuthorOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleListSerializer, UsersSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Класс обрабатывает запросы  GET, PATCH от авторизованных пользователей
    на просмотр или изменение данных своей учетной записи, а также обрабатывает
    запросы GET, POST, PATCH, DELETE от администратора.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Класс обрабатывает запросы POST от любого пользователя, осуществляет
    выдачу JWT-токена в обмен на валидные username и confirmation code.
    """

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Класс обрабатывает запросы POST от любого пользователя, выполняет
    валидацию уникальности полей email и username. После валидации
    пользователю на почту высылается подтверждающий код.
    """

    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        confirmation_code = str(uuid.uuid4())
        user = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'confirmation_code': confirmation_code}
        )
        email_body = (
            f'Код подтвержения для доступа к API: {user[0].confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user[0].email,
            'email_subject': 'Код подтвержения для доступа к API.'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    Класс обрабатывает запросы GET от любого пользователя,
    остальные методы POST, DELETE доступны только
    Администратору, обращение к конкретному обьекту
    происходит через уникальный slug. Возможен поиск
    через параметр name
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    Класс обрабатывает запросы GET от любого пользователя,
    остальные методы POST, DELETE доступны только
    Администратору, обращение к конкретному обьекту
    происходит через уникальный slug. Возможен поиск
    через параметр name
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Класс обрабатывает запросы GET от любого пользователя,
    остальные методы POST, PUT, PATCH, DELETE доступны только
    Администратору, реализован стандартный метод паджинации.
    """

    queryset = Title.objects.prefetch_related(
        'category', 'genre').annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        """
        Выбор сериализатора в зависимости от вида запроса
        """
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Класс обрабатывает запросы GET от любого пользователя, POST запросы
    доступны только авторизованным пользователям. Методы  PATCH,
    DELETE доступны только автору отзыва, модератору или админу,
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrAuthorOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Класс обрабатывает запросы GET от любого пользователя, POST запросы
    доступны только авторизованным пользователям. Методы  PATCH,
    DELETE доступны только автору комментария, модератору или админу,
    реализован стандартный метод паджинации.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthorOnly, IsAuthenticatedOrReadOnly]
    pagination_class = CommentsPaginator

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
