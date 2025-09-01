from rest_framework import serializers, exceptions
from blog.models import *


class BlogSerializer(serializers.ModelSerializer):
    
    tag = serializers.SerializerMethodField(method_name="edit_tag")
    status = serializers.SerializerMethodField(method_name="edit_status")



    class Meta :
        model = Blog
        fields = "__all__"


    def edit_tag(self,instance):
        id = instance.tag.id
        name = Tag.objects.get(id=id).name
        return name
    

    def edit_status(self, instance):
        if instance.status == True:
            return "تایید شده است"
        else:
            return "تایید نشده است"


