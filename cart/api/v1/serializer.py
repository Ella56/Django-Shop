from rest_framework import serializers, exceptions
from cart.models import *
from accounts.models import User




class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)  # if Product has price

    class Meta:
        model = OrderItems
        fields = [
            'id',
            'product_id',
            'product_name',
            'product_price',
            'quantity',
            'color',
            'guaranty',
            'created_at',
            'updated_at',
        ]


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = StatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        source='status',
        write_only=True,
        required=False
    )
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        source='profile',
        write_only=True
    )
    profile_email = serializers.EmailField(source='profile.user.email', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'profile_id',
            'profile_email',
            'is_paid',
            'status',
            'status_id',
            'total_price',
            'total_discount',
            'total_payment',
            'cart_hash',
            'cart_pan',
            'ref_id',
            'created_at',
            'updated_at',
            'items',
        ]
        read_only_fields = ['created_at', 'updated_at', 'items', 'profile_email']


class CreateOrderItemSerializer(serializers.ModelSerializer):
    """Used if you need to create OrderItems through API."""
    class Meta:
        model = OrderItems
        fields = ['cart', 'product', 'quantity', 'color', 'guaranty']
