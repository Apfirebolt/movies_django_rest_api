from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from movie.models import Movie, Game, Netflix
from accounts.models import CustomUser
from ecommerce.models import Item
from funds.models import Fund
from dinosaur.models import Dinosaur
from planets.models import Planet
from blog.models import (
    Blog,
    BlogPost,
    PostImage,
    BlogImage,
    Project,
    ProjectImages,
    GalleryPost,
    GalleryPostImages,
    Tags,
    GenericImage,
)
from books.models import Book
from lyrics.models import Lyrics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": (
            "No account exists with these credentials, check password and email"
        )
    }

    def validate(self, attrs):

        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data
        data.update(
            {
                "userData": {
                    "email": self.user.email,
                    "username": self.user.username,
                    "id": self.user.id,
                }
            }
        )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        min_length=8,
        style={"input_type": "password", "placeholder": "Password"},
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "id",
            "is_staff",
            "password",
            "access",
            "refresh",
        )

    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = (str(refresh.access_token),)
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ListCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "firstName",
            "lastName",
            "is_staff",
        )


class ListMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            "ID",
            "Movie_Name",
            "Year",
            "Timing",
            "Rating",
            "Votes",
            "Genre",
            "Language",
        )

    def validate(self, attrs):
        if attrs.get("Movie_Name") == "ABC":
            raise serializers.ValidationError("Movie_Name cannot be 'ABC'")
        return super().validate(attrs)

    def validate_Year(self, value):
        if value < 1900:
            raise serializers.ValidationError("Year cannot be less than 1900")
        return value

    def create(self, validated_data):
        return super().create(validated_data)


class ListGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = "__all__"


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ("name",)



class ListPostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = "__all__"

class ListBlogPostSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    @extend_schema_field(ListPostImageSerializer(many=True))
    def get_images(self, obj):
        images = obj.images.all()
        return ListPostImageSerializer(images, many=True).data
    

class ListBlogImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogImage
        fields = "__all__"


class ListBlogSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "author",
            "author_username",
            "date_posted",
            "date_updated",
            "views",
            "tags",
            "images",
        ]

    @extend_schema_field(ListBlogImageSerializer(many=True))
    def get_images(self, obj):
        # Cast to list before slicing to preserve the in-memory prefetch cache
        images = list(obj.images.all())[:3]
        return ListBlogImageSerializer(
            images, many=True, context=self.context
        ).data

    @extend_schema_field(TagListSerializer(many=True))
    def get_tags(self, obj):
        return TagListSerializer(
            obj.tags.all(), many=True, context=self.context
        ).data


class ListProjectImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectImages
        fields = "__all__"


class ListProjectSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    @extend_schema_field(ListProjectImageSerializer(many=True))
    def get_images(self, obj):
        # maximum of 2 images
        images = obj.images.all()[:3]
        return ListProjectImageSerializer(
            images, many=True, context=self.context
        ).data

    @extend_schema_field(TagListSerializer(many=True))
    def get_tags(self, obj):
        tags = obj.tags.all()
        return TagListSerializer(tags, many=True, context=self.context).data


class DetailProjectSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    @extend_schema_field(ListProjectImageSerializer(many=True))
    def get_images(self, obj):
        images = obj.images.all()
        return ListProjectImageSerializer(
            images, many=True, context=self.context
        ).data

    @extend_schema_field(TagListSerializer(many=True))
    def get_tags(self, obj):
        tags = obj.tags.all()
        return TagListSerializer(tags, many=True, context=self.context).data


class ListGalleryPostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GalleryPostImages
        fields = "__all__"


class ListGalleryPostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = GalleryPost
        fields = "__all__"

    @extend_schema_field(ListGalleryPostImageSerializer(many=True))
    def get_images(self, obj):
        images = list(obj.images.all())[:3]
        return ListGalleryPostImageSerializer(
            images, many=True, context=self.context
        ).data

    @extend_schema_field(TagListSerializer(many=True))
    def get_tags(self, obj):
        return TagListSerializer(
            obj.tags.all(), many=True, context=self.context
        ).data


class DetailGalleryPostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = GalleryPost
        fields = "__all__"

    @extend_schema_field(ListGalleryPostImageSerializer(many=True))
    def get_images(self, obj):
        images = obj.images.all()
        return ListGalleryPostImageSerializer(
            images, many=True, context=self.context
        ).data

    @extend_schema_field(TagListSerializer(many=True))
    def get_tags(self, obj):
        return TagListSerializer(
            obj.tags.all(), many=True, context=self.context
        ).data


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = "__all__"


class GenericImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericImage
        fields = "__all__"


class ListItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"


class ListNetflixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Netflix
        fields = "__all__"


class ListFundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fund
        fields = "__all__"


class ListDinosaurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dinosaur
        fields = "__all__"


class ListPlanetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Planet
        fields = [
            "planet_name",
            "planet_host",
            "num_stars",
            "num_planets",
            "discovery_method",
            "discovery_year",
            "discovery_facility",
            "spectral_type",
            "stellar_metallicity_ratio",
        ]


class ListBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class ListLyricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lyrics
        fields = "__all__"