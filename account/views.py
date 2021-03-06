from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, PermissionSerializer, ChangeEmailSerializer
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, Permission
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from django.views.generic import TemplateView
from django_email_verification import send_email
from django.conf import settings

from .utils import user_utils


# Authentication APIs
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = serializer.save()
        send_email(user)
        return Response({"success": True}, status=status.HTTP_201_CREATED)


# User APIs
class UpdateUserAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            update_user_serializer = UserSerializer(request.user, data=request.data)
            if not update_user_serializer.is_valid():
                return Response(update_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = update_user_serializer.save()
        except Exception as error:
            response = {
                "success": False,
                "message": str(error),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UsersListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Permission APIs
class PermissionsListAPI(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]


class PermissionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
      Handles password reset tokens
      When a token is created, an e-mail needs to be sent to the user
      :param sender: View Class that sent the signal
      :param instance: View Instance that sent the signal
      :param reset_password_token: Token Model Object
      :param args:
      :param kwargs:
      :return:
      """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format('localhost:8000/profiles/password-reset-form', reset_password_token.key),
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset Request",
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_FROM_ADDRESS,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class ResetPasswordForm(TemplateView):
    template_name = 'reset_password.html'

    def get_context_data(self, **kwargs):
        token = self.request.GET.get('token')
        context = {"token": token}
        return context


class ChangeEmailView(generics.GenericAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            change_email_serializer = ChangeEmailSerializer(request.user, data=request.data)
            if not change_email_serializer.is_valid():
                return Response(change_email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = change_email_serializer.save()
        except Exception as error:
            response = {
                "success": False,
                "message": str(error),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # Send Verification Email
        send_email(user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
