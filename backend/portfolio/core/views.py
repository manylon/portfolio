from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from wagtail.models import PageViewRestriction
from .serializers import (
    PasswordFormSerializer,
    PasswordRestrictionSerializer,
)

class AuthenticateWithPassword(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    @method_decorator(csrf_protect)
    def post(self, request, app_name, slug):
        """
        Authenticate with a shared password and return the protected content.
        Works only for password-protected pages.

        Args:
            request (Request): The request object containing the password.
            app_name (str): The name of the app.
            slug (str): The slug of the page.

        Returns:
            Response: The response containing the protected content or an error message.
        """
        if app_name in settings.LOCAL_APPS:
            model, serializer = self.get_model_and_serializer(app_name)
            if not model:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            obj = model.objects.live().get(slug=slug)
        except model.DoesNotExist:
            return Response(
                {"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND
            )

        restriction = obj.get_view_restrictions().first()

        if restriction and restriction.restriction_type == PageViewRestriction.PASSWORD:
            password_serializer = PasswordFormSerializer(data=request.data)

            if password_serializer.is_valid():
                provided_password = password_serializer.validated_data.get("password")

                password_serializer = PasswordRestrictionSerializer(
                    data={"password": provided_password}, restriction=restriction
                )

                if password_serializer.is_valid():
                    response = serializer(obj)
                    return Response(response.data)

                return Response(
                    {"detail": "Incorrect password."}, status=status.HTTP_403_FORBIDDEN
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "No password protection found."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_model_and_serializer(self, app_name):
        """
        Returns the correct model and serializer based on the app name.
        """
        if app_name == "blog":
            from blog.models import BlogPostPage
            from blog.serializers import BlogPostSerializer

            return BlogPostPage, BlogPostSerializer
        return None, None
