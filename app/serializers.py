from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, EmailValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import PrimaryKeyRelatedField

from app.models import User, admin, ScenicSpot, Hotel, Product, ProductOrder, ScenicSpotOrder, HotelOrder
from rest_framework.serializers import ModelSerializer, SerializerMethodField


# 序列化器主要是对字段的一个限制

# def length_validate(value):
#     if not(10 < len(value) < 20):
#         raise serializers.ValidationError("字段的长度不在10-20之间")


class UserSerializer(ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = '__all__'

        # 数据库字段

    username = serializers.CharField(
        validators=[
            MinLengthValidator(2, message='用户名必须至少包含两个字符。'),
            MaxLengthValidator(10, message='用户名不能超过十个字符.')
        ],
        required=False
    )

    password = serializers.CharField(
        validators=[
            MinLengthValidator(10, message='密码必须至少包含十个字符。'),
            MaxLengthValidator(20, message='密码不能超过二十个字符.'),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z]).*$',
                message='密码必须包含至少一个小写字母和一个大写字母。'
            ),
        ],
        required=False
    )

    email = serializers.EmailField(
        required=False
    )

    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?:\+?86)?1[3-9]\d{9}$',
                message='请输入有效的手机号码。'
            )
        ],
        required=False
    )


# 管理员
class adminSerializer(ModelSerializer):
    class Meta:
        model = admin
        fields = '__all__'


# 景区
def validate_name(value):
    # 对景点名称进行长度限制
    if len(value) < 2:
        raise serializers.ValidationError("景点名称太短")
    return value


def validate_ticket_price(value):
    # 对门票价格进行验证
    if value <= 0:
        raise serializers.ValidationError("门票价格必须大于0")
    return value


class ScenicSpotSerializer(ModelSerializer):
    class Meta:
        model = ScenicSpot
        fields = '__all__'


# 酒店
class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


# 产品
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# # 评论
# class ReviewSerializer(ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'


class ScenicSpotOrderSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ScenicSpot = serializers.PrimaryKeyRelatedField(queryset=ScenicSpot.objects.all())

    class Meta:
        model = ScenicSpotOrder
        fields = ['id', 'user', 'ScenicSpot', 'quantity', 'total_price', 'order_date', "status"]


class HotelOrderSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    class Meta:
        model = HotelOrder
        fields = ['id', 'user', 'hotel', 'quantity', 'total_price', 'order_date', "status"]



class ProductOrderSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductOrder
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'order_date', "status"]





