from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    JWTTokenSerializer,
    ReviewsSerializer,
    TitlesListSerializer,
    TitlesSerializer,
    UserEmailSerializer,
    UserSerializer,
)
from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Review, Title
from users.models import User
from .permissions import IsAdmin, IsAuthorOrReadOnly, IsModerator, ReadOnly


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet, ):
    pass


class CategoriesViewSet(CreateDeleteViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdmin | ReadOnly,)


class GenresViewSet(CreateDeleteViewSet):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdmin | ReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    filterset_class = TitleFilter

    permission_classes = (IsAdmin | ReadOnly,)

    def get_serializer_class(self):
        if self.action in (
                "create",
                "partial_update",
        ):
            return TitlesSerializer
        return TitlesListSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    permission_classes = (IsAdmin,)

    @action(detail=False, methods=["get", "patch"],
            url_path="me", url_name="me",
            permission_classes=[IsAuthenticated])
    def about_me(self, request, pk=None):

        serializer = UserSerializer(request.user)

        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        serializer.save(title=title, author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        serializer.save(review=review, author=self.request.user)


class SignUp(APIView):
    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user, created = User.objects.get_or_create(**serializer.data)
        encoded = default_token_generator.make_token(current_user)

        subject = "Confirmation code from YaMDb"
        message = f"{encoded} - ваш код для авторизации на YaMDb"
        admin_email = ADMIN_EMAIL
        user_email = [current_user.email]
        send_mail(subject, message, admin_email, user_email)

        return Response(serializer.data)


class JWTTokenViewSet(APIView):
    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user = get_object_or_404(
            User, username=serializer.data["username"]
        )
        confirmation_code = default_token_generator.make_token(current_user)
        if confirmation_code != serializer.data["confirmation_code"]:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(current_user)
        return Response({"token": str(refresh.access_token)})
