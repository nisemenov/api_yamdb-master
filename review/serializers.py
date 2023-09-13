from rest_framework import serializers
from review.models import Review, Comment, Title, Genre, Category
from django.db.models import Avg, Q


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category

    def create(self, validated_data):
        name = validated_data.get('name', '')
        slug = validated_data.get('slug', '')
        if Category.objects.filter(Q(name=name) | Q(slug=slug)).exists():
            raise serializers.ValidationError(
                'This category already exists.'
            )
        return super().create(validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def create(self, validated_data):
        name = validated_data.get('name', '')
        slug = validated_data.get('slug', '')
        if Genre.objects.filter(Q(name=name) | Q(slug=slug)).exists():
            raise serializers.ValidationError(
                'This genre already exists.'
            )
        return super().create(validated_data)


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
