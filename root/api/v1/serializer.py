from rest_framework import serializers
from root.models import *


class TeamSerializer(serializers.ModelSerializer):

    skills = serializers.PrimaryKeyRelatedField(queryset=Skills.objects.all(), write_only=True)
    skills_name = serializers.CharField(source="skills.name", read_only=True)

    class Meta:
        model = Team
        fields = "__all__"




class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"




class FaqSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"