from rest_framework import serializers, exceptions
from product.models import *
from accounts.models import User


class ProductSerializer(serializers.ModelSerializer):
    # write-only field: accepts category ID on create/update
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    # read-only field: shows category name on GET
    category_name = serializers.CharField(source="category.name", read_only=True)
    color = serializers.SlugRelatedField(many =True, queryset = Color.objects.all(), slug_field="color")
    guaranty = serializers.SlugRelatedField(many =True, queryset = Guaranty.objects.all(), slug_field="months")
    has_discount =serializers.SerializerMethodField(method_name="edit_has_discount")
    has_guaranty =serializers.SerializerMethodField(method_name="edit_has_guaranty")
    has_color = serializers.SerializerMethodField(method_name="edit_has_color")
    availability = serializers.SerializerMethodField(method_name="edit_availability")


    class Meta:
        model = Product
        fields = "__all__"
    
    
    def edit_has_discount(self, instance):
        return "تخفیف دارد" if instance.has_discount else "تخفیف ندارد"


    def edit_has_guaranty(self, instance):
        return "گارانتی دارد" if instance.has_guaranty else "گارانتی ندارد"
  

    def edit_has_color(self, instance):
        return "رنگبندی دارد" if instance.has_color else "رنگبندی ندارد"


    def edit_availability(self, instance):
        return "موجود است" if instance.availability else "موجود نیست"
        




class ProductCommentSerializer(serializers.ModelSerializer):
    # writeable fields
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    name = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    # read-only fields
    product_name = serializers.CharField(source="product.name", read_only=True)
    user_name = serializers.CharField(source="name.user.email", read_only=True)
    status = serializers.SerializerMethodField(method_name="edit_status")


    class Meta :
        model = Comment
        fields = [
            "id",
            "product",       # for POST (ID)
            "name",          # for POST (ID)
            "comment",
            "created_at",
            "updated_at",
            "status",
            "product_name",  # for GET (name)
            "user_name",     # for GET (username)
        ]
        read_only_fields = ["created_at", "updated_at", "status"]


    def edit_status(self, instance):
        return "تایید شده است" if instance.status else "در انتظار تایید"

