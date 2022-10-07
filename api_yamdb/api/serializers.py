import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User, вызывается  при обращении к
    конкретному обьекту или изменении данных пользователей.
    """
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio',)


class NotAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User, вызывается GET, PATH запросах
    зарегистрированного пользователя к данным своей учетной записи.
    """

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio',)
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User, вызывается при POST запросе
    на получение JWT-токена в обмен на username и confirmation code.
    """
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User, вызывается при POST-запросе на регистрацию
    нового пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category. Уникальность поля slug
    проветяется на уровне модели и в сериализаторе.
    """

    class Meta:
        model = Category
        exclude = ('id',)

        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['slug', ],
                message='Категория уже существует',
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Genre. Уникальность поля slug
    проветяется на уровне модели и в сериализаторе.
    """

    class Meta:
        model = Genre
        exclude = ('id',)

        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['slug', ],
                message='Жанр уже существует',
            )
        ]


class TitleListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title, вызывается при GET запросе списка или
    конкретного обьекта поля genre и category вложенные сериализаторы,
    поле rating получается подсчетом среднего значения
    поля score из модели Review.
    """
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title, вызывается при обращении к
    конкретному обьекту или изменении данных,
    поля genre и category берут slug значения из соответсвующих
    моделей, поле rating получается подсчетом среднего значения
    поля rating из модели Review, проводится валидация поля
    year исключая передачу года выше текущего.
    """
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', ],
                message='Произведение уже в базе',
            )
        ]

    def validate_year(self, value):
        """
        Валидация на то что бы год выпуска не был выше текущего
        """
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Review, вызывается при обращении к
    конкретному обьекту или изменении данных,
    полe title_id берет значение из модели Title,
    производится валидация поля score и проверка на то,
    что только один отзыв к конкретному произведению
    """
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        """ Валидация на то поставлена допустимая оценка. """
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Вы можете поставить оценку от 1 до 10 баллов!'
            )
        return value

    def validate(self, data):
        """ Валидация на то, что один автор может оставить
        только один отзыв к конкретному произведению. """
        author = self.context['request'].user
        title = get_object_or_404(
            Title,
            pk=self.context.get('view').kwargs.get('title_id')
        )
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли рецензию на это произведение!'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Comment, вызывается при обращении к
    конкретному обьекту или изменении данных,
    полe title_id и review_id берут значения из соответствующих моделей.
    """
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
