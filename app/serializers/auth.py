from django.contrib.auth import get_user_model
from rest_auth.serializers import TokenSerializer, UserDetailsSerializer
from rest_framework.authtoken.models import Token


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'username')


class CustomTokenSerializer(TokenSerializer):
    user = CustomUserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
