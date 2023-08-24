from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='review')
    title = models.ForeignKey('Title', on_delete=models.CASCADE,
                              blank=True, null=True,
                              related_name='review',
                              verbose_name='titles')

    def __str__(self):
        return self.text


class Title(models.Model):



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    text = models.TextField()
    created = models.DateTimeField('Date of create',
                                   auto_now_add=True, db_index=True)


class Category(models.Model):
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return self.title


class Genre(models.Model):