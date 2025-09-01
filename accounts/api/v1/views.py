from rest_framework.generics import GenericAPIView
from accounts.models import User, Profile
from rest_framework.response import Response
from .serializer import SignupSerializer, CustomAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



class SignUpApiView(GenericAPIView):
    serializer_class = SignupSerializer


    def post(self,request, *args, **kwargs):
        serialize = self.serializer_class(data = request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({"message" : "ثبت نام با موفقیت انجام شد."
        ""})
    


class LoginApiView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key, 'email':user.email})