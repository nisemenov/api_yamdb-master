from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from review.models import Review, Comment, Title, Genre, Category
from django.db.models import Avg, Q


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def create(self, validated_data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            author=user,
            title=Title.objects.get(id=title_id)
        ).exists():
            raise serializers.ValidationError('You have already created such '
                                              'review.')
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerList(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        avg_rating = (obj.review.aggregate(Avg('score'))['score__avg'])
        if avg_rating is not None:
            return round(avg_rating, 2)
        return None


class TitleSerializerDetail(TitleSerializerList):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=False
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
