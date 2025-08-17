from rest_framework import serializers, exceptions
from accounts.models import User
from django.contrib.auth.password_validation import validate_password






class SignupSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email','password']


    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'message' : list(e.messages)})
        return super().validate(attrs)
    


    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(email,password)
        return user