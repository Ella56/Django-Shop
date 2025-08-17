from rest_framework.generics import GenericAPIView
from accounts.models import User, Profile
from rest_framework.response import Response
from .serializer import SignupSerializer



class SignUpApiView(GenericAPIView):
    serializer_class = SignupSerializer


    def post(self,request, *args, **kwargs):
        serialize = self.serializer_class(data = request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response({"message" : "ثبت نام با موفقیت انجام شد."
        ""})