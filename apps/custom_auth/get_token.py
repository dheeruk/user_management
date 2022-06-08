from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.six import text_type
import datetime

TOKEN_LIFETIME = datetime.timedelta(weeks=13)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        refresh = super().get_token(user)
        new_token = refresh.access_token
        new_token.set_exp(lifetime=TOKEN_LIFETIME)
        return {
            "id":user.id,
            "email":user.email,
            "access":text_type(new_token),
            "refresh":text_type(refresh),
            "first_name":user.first_name,
            "last_name":user.last_name,
            "status":user.status            
        }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer