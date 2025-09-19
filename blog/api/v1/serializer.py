from rest_framework import serializers, exceptions
from blog.models import *
from accounts.models import User


class BlogSerializer(serializers.ModelSerializer):

    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True)
    status = serializers.SerializerMethodField(method_name="edit_status")



    class Meta :
        model = Blog
        fields = "__all__"


    def edit_status(self, instance):
        if instance.status == True:
            return "تایید شده است"
        else:
            return "تایید نشده است"
        


class CommentSerializer(serializers.ModelSerializer):
    # writeable fields
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
    name = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    # read-only fields
    blog_name = serializers.CharField(source="blog.name", read_only=True)
    user_name = serializers.CharField(source="name.user.email", read_only=True)
    status = serializers.SerializerMethodField(method_name="edit_status")


    class Meta :
        model = Blog_Comment
        fields= [
            "id",
            "blog",       # for POST (ID)
            "name",          # for POST (ID)
            "comment",
            "created_at",
            "updated_at",
            "status",
            "blog_name",  # for GET (name)
            "user_name",     # for GET (username)
        ]
        read_only_fields = ["created_at", "updated_at", "status"]

    

    def edit_status(self, instance):
        return "تایید شده است" if instance.status else "در انتظار تایید"


