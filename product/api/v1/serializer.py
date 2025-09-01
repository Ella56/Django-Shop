from rest_framework import serializers, exceptions
from product.models import *


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(method_name="edit_category")
    color = serializers.SlugRelatedField(many =True, queryset = Color.objects.all(), slug_field="color")
    guaranty = serializers.SlugRelatedField(many =True, queryset = Guaranty.objects.all(), slug_field="months")
    has_discount =serializers.SerializerMethodField(method_name="edit_has_discount")
    has_guaranty =serializers.SerializerMethodField(method_name="edit_has_guaranty")
    has_color = serializers.SerializerMethodField(method_name="edit_has_color")
    availability = serializers.SerializerMethodField(method_name="edit_availability")


    class Meta:
        model = Product
        fields = "__all__"

        

    def edit_category(self, instance):
        id = instance.category.id
        name = Category.objects.get(id=id).name
        return name
    
    def edit_has_discount(self, instance):
        if instance.has_discount == True:
            return "تخفیف دارد"
        else:
            return "تخفیف ندارد"

    def edit_has_guaranty(self, instance):
        if instance.has_guaranty == True:
            return "گارانتی دارد"
        else:
            return "گارانتی ندارد"

    def edit_has_color(self, instance):
        if instance.has_color == True:
            return "رنگبندی دارد"
        else:
            return "رنگبندی ندارد"

    def edit_availability(self, instance):
        if instance.availability == True:
            return "موجود است"
        else:
            return "موجود نیست"

