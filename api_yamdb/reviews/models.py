from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Category(models.Model):
    """
    Модель для управления категориями произведений. Включает наименование
    категории и slug по которому доступна конкретная категория.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя',
        help_text=('Уникально имя должно содержать '
                   'только Латинские буквы и цифры')
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=['slug', ],
                name='unique_category'
            ),
        ]

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """
    Модель для управления жанрами произведений. Включает наименование жанра и
    slug по которому доступен конкретный жанр.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя',
        help_text=('Уникально имя должно содержать '
                   'только Латинские буквы и цифры')
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=['slug', ],
                name='unique_genre'
            ),
        ]

    def __str__(self):
        return self.slug


class Title(models.Model):
    """
    Модель для управления произведениями. Включает название произведения,
    год создания, описание, категорию и жанр.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выхода'
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='title',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=['name', 'category'],
                name='unique_title'
            ),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель для управления отзывами на произведения. Позволяет пользователям
    оставлять отзывы на  произведения и выставлять оценки. Включает автора,
    название произведения, дату публикации, текст рецензии, оценку (1 до 10).
    Автор может оставить только один отзыв к каждому конкретному произведению.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    text = models.CharField(max_length=200)

    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(MaxValueValidator(10), MinValueValidator(1)),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для управления комментариями. Позволяет пользователям комментировать
    рецензии. Включает автора комментария, дату публикации, произведение,
    и текст комментария.  Комментарий привязан к определённому отзыву.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        verbose_name='Комментарий',
        max_length=200
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
