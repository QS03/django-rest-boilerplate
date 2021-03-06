from django.contrib.auth import authenticate
from account.models import User


def get_user_or_None(email, password):
    user = authenticate(email=email, password=password)
    if user is not None:
        return user
    return None


def validate_unique_email(current_email, new_email):
    if current_email == new_email:
        return
    if User.objects.filter(email=new_email).exists():
        raise Exception("Email already exist.")


def validate_unique_username(current_username, new_username):
    if current_username == new_username:
        return
    if User.objects.filter(username=new_username).exists():
        raise Exception("Username already exist.")
