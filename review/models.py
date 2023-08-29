from django.db import models
from users.models import User


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.IntegerField()

    def __str__(self):
        return self.text


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='title'
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='title'
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField('Slug', blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField('Slug', blank=True, null=True)

    def __str__(self):
        return self.name
