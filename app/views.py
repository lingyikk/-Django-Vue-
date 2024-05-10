from datetime import datetime
from itertools import chain

from dateutil.parser import parse
from django.contrib.auth import authenticate
from django.shortcuts import render

from tokenize import TokenError

from cryptography.fernet import InvalidToken
from django.http import HttpResponse, JsonResponse, FileResponse
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
# from serve.settings import MEDIA_ROOT
from .models import User, admin, ScenicSpot, Hotel, Product, ProductOrder, ScenicSpotOrder, HotelOrder
from .serializers import UserSerializer, adminSerializer, ScenicSpotSerializer, HotelSerializer, \
    ProductSerializer, ProductOrderSerializer, ScenicSpotOrderSerializer, HotelOrderSerializer

# 视图函数中所需导入的内容
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
# 封装的状态码 - 不写status数字了
from rest_framework import status, viewsets
from rest_framework.views import APIView
# 使用视图集 GenericAPIView
from rest_framework.generics import GenericAPIView, get_object_or_404
# 使用视图扩展类的-基本扩展类
from rest_framework import mixins
# 使用视图扩展类的-视图扩展类
from rest_framework import generics
# 使用视图集类
from rest_framework.viewsets import ModelViewSet, GenericViewSet
# 登录认证
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# 过滤器类
# from app.filter import UserFilter
# 排序过滤器
from rest_framework.filters import OrderingFilter
# 日期格式化
from datetime import datetime

# 分页器
from app.PagePagination import UserPagination


# def format_datetime(timestamp):
#     if isinstance(timestamp, datetime):
#         return timestamp.strftime('%Y-%m-%d %H:%M:%S')
#     return timestamp  # 如果不是datetime对象，则直接返回原值


# order_date日期格式
def format_datetime(data):
    formatted_data = []
    for order in data:
        if isinstance(order['order_date'], datetime):
            order['order_date'] = order['order_date'].strftime('%Y-%m-%d %H:%M:%S')
        formatted_data.append(order)
    return formatted_data


class UserViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        filtered_data = []
        for item in data:
            datetime_str = item['registration_date']
            parsed_datetime = parse(datetime_str)
            formatted_str = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")

            filtered_item = {
                'id': item['id'],
                'username': item['username'],
                'password': item['password'],
                'email': item['email'],
                'phone_number': item['phone_number'],
                'registration_date': formatted_str,
            }
            filtered_data.append(filtered_item)

        # 获取字段宽度
        field_widths = {
            'id': '50',
            'username': '120',
            'password': '120',
            'email': '200',
            'phone_number': '150',
            'registration_date': 'auto',
            # 添加其他字段
        }

        # 获取模型字段数据
        model_fields = User._meta.get_fields()
        form_data = [
            {'property': field.name, 'label': field.verbose_name, 'width': field_widths.get(field.name, 'auto')}
            for field in model_fields
            if not field.auto_created
        ]

        # 构建返回的数据
        user_data = {
            'message': '自定义响应数据',
            'status': 200,
            'data': {
                "data": filtered_data,
                "form_data": form_data,
            }
        }
        return Response(user_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        queryset = self.get_queryset()
        serialized_data = self.get_serializer(queryset, many=True)

        username_orders = User.objects.all().values(
            'id', 'username', 'password', 'email', 'phone_number', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)

        response_data = {
            "data": username_orders,
            "status": 200,
            "message": "Object created successfully"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 获取更新后的最新数据
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        username_orders = User.objects.all().values(
            'id', 'username', 'password', 'email', 'phone_number', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)
        response_data = {
            "data": username_orders,
            "status": 200
        }
        return Response(response_data, status=status.HTTP_200_OK)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        username_orders = User.objects.all().values(
            'id', 'username', 'password', 'email', 'phone_number', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)

        response_data = {
            "data": username_orders,
            "status": 200
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # 模糊查询用户名
    @action(detail=False, methods=['get'], url_path='search')
    def search_user(self, request):
        username = request.query_params.get('username', '').strip()
        if username:
            users = User.objects.filter(username__icontains=username)
            serializer = self.get_serializer(users, many=True)

            # 格式化日期时间字段
            formatted_data = []
            for item in serializer.data:
                formatted_item = item.copy()
                formatted_item['registration_date'] = parse(item['registration_date']).strftime('%Y-%m-%d %H:%M:%S')
                formatted_data.append(formatted_item)
            return Response(formatted_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

    # 登录
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        if user.password == password:
            data = {
                'isLogin': "true",
                'username': username
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'isLogin': "false"},
                            status=status.HTTP_400_BAD_REQUEST)

    # 注册
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({'message': '该用户已存在'}, status=status.HTTP_400_BAD_REQUEST)
        # 创建用户
        user = User.objects.create(username=username, password=password)
        # 返回成功响应
        data = {
            'username': user.username,
            'isRegister': 'true',
        }
        return Response(data, status=status.HTTP_200_OK)


class adminViews(ModelViewSet):
    queryset = admin.objects.all()
    serializer_class = adminSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        filtered_data = []
        for item in data:
            datetime_str = item['registration_date']
            parsed_datetime = parse(datetime_str)
            formatted_str = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")

            filtered_item = {
                'id': item['id'],
                'username': item['username'],
                'password': item['password'],
                'registration_date': formatted_str,
            }
            filtered_data.append(filtered_item)

        # 构建返回的数据
        user_data = {
            'message': '自定义响应数据',
            'status': 200,
            'data': filtered_data
        }
        return Response(user_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        queryset = self.get_queryset()
        serialized_data = self.get_serializer(queryset, many=True)

        username_orders = admin.objects.all().values('id', 'username', 'password', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)

        response_data = {
            "data": username_orders,
            "status": 200,
            "message": "Object created successfully"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 获取更新后的最新数据
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        username_orders = admin.objects.all().values('id', 'username', 'password', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)
        response_data = {
            "data": username_orders,
            "status": 200
        }
        return Response(response_data, status=status.HTTP_200_OK)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        username_orders = admin.objects.all().values('id', 'username', 'password', 'registration_date')
        formatted_data = []
        for order in username_orders:
            if isinstance(order['registration_date'], datetime):
                order['registration_date'] = order['registration_date'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_data.append(order)

        response_data = {
            "data": username_orders,
            "status": 200
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # 模糊查询用户名
    @action(detail=False, methods=['get'], url_path='search')
    def search_user(self, request):
        username = request.query_params.get('username', '').strip()
        if username:
            users = admin.objects.filter(username__icontains=username)
            serializer = self.get_serializer(users, many=True)

            # 格式化日期时间字段
            formatted_data = []
            for item in serializer.data:
                formatted_item = item.copy()
                formatted_item['registration_date'] = parse(item['registration_date']).strftime('%Y-%m-%d %H:%M:%S')
                formatted_data.append(formatted_item)

            return Response({"data": formatted_data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username').strip()
        password = request.data.get('password').strip()
        if admin.objects.filter(username=username).exists():
            try:
                user = admin.objects.get(username=username)
                if user.password == password:
                    data = {
                        'isLogin': "true",
                        'username': username
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'isLogin': "false"}, status=status.HTTP_400_BAD_REQUEST)
            except admin.DoesNotExist:
                return Response({'isLogin': "false"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'isLogin': "false"}, status=status.HTTP_400_BAD_REQUEST)

    # 注册
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # 检查用户名是否已存在
        if admin.objects.filter(username=username).exists():
            return Response({'message': '用户已存在'}, status=status.HTTP_400_BAD_REQUEST)
        # 创建用户
        user = admin.objects.create(username=username, password=password)
        # 返回成功响应
        data = {
            'usernames': user.username,
            'isRegister': 'true',
        }
        return Response(data, status=status.HTTP_200_OK)


class ScenicSpotViews(ModelViewSet):
    queryset = ScenicSpot.objects.all()
    serializer_class = ScenicSpotSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        all_scenic_spots = ScenicSpot.objects.all()
        all_serializer = self.get_serializer(all_scenic_spots, many=True)
        data = {
            'newData': all_serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        all_scenic_spots = ScenicSpot.objects.all()
        all_serializer = self.get_serializer(all_scenic_spots, many=True)

        return Response(all_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        all_scenic_spots = ScenicSpot.objects.all()
        all_serializer = self.get_serializer(all_scenic_spots, many=True)

        return Response(all_serializer.data, status=status.HTTP_200_OK)

    # 模糊查询景区名
    @action(detail=False, methods=['get'], url_path='search')
    def search_ScenicSpot(self, request):
        name = request.query_params.get('name', '').strip()
        if name:
            users = ScenicSpot.objects.filter(name__icontains=name)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"},
                            status=status.HTTP_400_BAD_REQUEST)


class HotelViews(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        all_scenic_spots = Hotel.objects.all()
        all_serializer = self.get_serializer(all_scenic_spots, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        all_hotels = Hotel.objects.all()
        all_serializer = self.get_serializer(all_hotels, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    # 模糊查询酒店名称
    @action(detail=False, methods=['get'], url_path='search')
    def search_hotel(self, request):
        hotel_name = request.query_params.get('hotel_name', '').strip()
        if hotel_name:
            hotels = Hotel.objects.filter(name__icontains=hotel_name)
            serializer = self.get_serializer(hotels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a hotel_name parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        all_hotels = Hotel.objects.all()
        all_serializer = self.get_serializer(all_hotels, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)


class ProductViews(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        all_products = Product.objects.all()
        all_serializer = self.get_serializer(all_products, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        all_products = Product.objects.all()
        all_serializer = self.get_serializer(all_products, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    # 模糊查询产品名称
    @action(detail=False, methods=['get'], url_path='search')
    def search_product(self, request):
        name = request.query_params.get('Product_name', '').strip()
        if name:
            products = Product.objects.filter(name__icontains=name)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a name parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        all_products = Product.objects.all()
        all_serializer = self.get_serializer(all_products, many=True)
        data = {
            'newData': all_serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)


class ScenicSpotOrderViews(ModelViewSet):
    queryset = ScenicSpotOrder.objects.all()
    serializer_class = ScenicSpotOrderSerializer

    def list(self, request, *args, **kwargs):
        scenic_spot_orders = ScenicSpotOrder.objects.all().values(
            'id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(scenic_spot_orders)
        return Response(scenic_spot_orders)

    def create(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        scenic_spot_name = request.data.get('ScenicSpot')
        print(user_name)
        print(scenic_spot_name)
        # 获取关联对象或返回404
        user = get_object_or_404(User, username=user_name)
        scenic_spot = get_object_or_404(ScenicSpot, name=scenic_spot_name)

        request.data.pop('user')
        request.data.pop('ScenicSpot')

        # 创建订单
        request.data['user'] = user.id
        request.data['ScenicSpot'] = scenic_spot.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        scenic_spot_orders = ScenicSpotOrder.objects.all().values(
            'id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(scenic_spot_orders)

        data = {
            'newData': scenic_spot_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        scenic_spot_name = request.data.get('ScenicSpot')

        # 获取关联对象或返回404
        user = get_object_or_404(User, username=user_name)
        scenic_spot = get_object_or_404(ScenicSpot, name=scenic_spot_name)

        instance = self.get_object()
        instance.user = user
        instance.ScenicSpot = scenic_spot
        instance.quantity = request.data.get('quantity')
        instance.total_price = request.data.get('total_price')
        instance.save()

        scenic_spot_orders = ScenicSpotOrder.objects.all().values(
            'id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(scenic_spot_orders)

        data = {
            'newData': scenic_spot_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        scenic_spot_orders = ScenicSpotOrder.objects.all().values(
            'id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(scenic_spot_orders)

        data = {
            'newData': scenic_spot_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search_ScenicSpotOrder(self, request):
        username = request.query_params.get('username', '').strip()
        if username:
            scenic_spot_orders = ScenicSpotOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
            format_datetime(scenic_spot_orders)

            return Response(scenic_spot_orders, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"}, status=status.HTTP_400_BAD_REQUEST)


class HotelOrderViews(ModelViewSet):
    queryset = HotelOrder.objects.all()
    serializer_class = HotelOrderSerializer

    def list(self, request, *args, **kwargs):
        hotel_orders = HotelOrder.objects.all().values(
            'id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(hotel_orders)
        return Response(hotel_orders, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        hotel_name = request.data.get('hotel')
        user = get_object_or_404(User, username=user_name)
        hotel = get_object_or_404(Hotel, name=hotel_name)
        request.data.pop('user')
        request.data.pop('hotel')
        request.data['user'] = user.id
        request.data['hotel'] = hotel.id
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        hotel_orders = HotelOrder.objects.all().values(
            'id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(hotel_orders)

        data = {
            'newData': hotel_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        hotel_name = request.data.get('hotel')

        # 获取关联对象或返回404
        user = get_object_or_404(User, username=user_name)
        hotel = get_object_or_404(Hotel, name=hotel_name)

        instance = self.get_object()
        instance.user = user
        instance.hotel = hotel
        instance.quantity = request.data.get('quantity')
        instance.total_price = request.data.get('total_price')
        instance.status = request.data.get('status')
        instance.save()

        hotel_orders = HotelOrder.objects.all().values(
            'id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(hotel_orders)

        data = {
            'newData': hotel_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        hotel_orders = HotelOrder.objects.all().values(
            'id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(hotel_orders)

        data = {
            'newData': hotel_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search_HotelOrder(self, request):
        username = request.query_params.get('username', '').strip()
        if username:
            hotel_orders = HotelOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
            format_datetime(hotel_orders)

            return Response(hotel_orders, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"}, status=status.HTTP_400_BAD_REQUEST)


class ProductOrderViews(ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def list(self, request, *args, **kwargs):
        product_orders = ProductOrder.objects.all().values(
            'id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', "status")
        format_datetime(product_orders)

        return Response(product_orders)

    def create(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        product_name = request.data.get('product')
        user = get_object_or_404(User, username=user_name)
        product = get_object_or_404(Product, name=product_name)

        request.data.pop('user')
        request.data.pop('product')

        # 创建订单
        request.data['user'] = user.id
        request.data['product'] = product.id
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        product_orders = ProductOrder.objects.all().values(
            'id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', 'status')
        format_datetime(product_orders)

        data = {
            'newData': product_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_name = request.data.get('user')
        product_name = request.data.get('product')

        # 获取关联对象或返回404
        user = get_object_or_404(User, username=user_name)
        product = get_object_or_404(Product, name=product_name)

        instance = self.get_object()
        instance.user = user
        instance.product = product
        instance.quantity = request.data.get('quantity')
        instance.total_price = request.data.get('total_price')
        instance.status = request.data.get('status')
        instance.save()

        product_orders = ProductOrder.objects.all().values(
            'id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', "status")
        format_datetime(product_orders)
        data = {
            'newData': product_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        product_orders = ProductOrder.objects.all().values(
            'id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', "status")
        format_datetime(product_orders)
        data = {
            'newData': product_orders,
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search_ProductOrder(self, request):
        username = request.query_params.get('username', '').strip()
        if username:
            product_orders = ProductOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', "status")
            format_datetime(product_orders)

            return Response(product_orders, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"}, status=status.HTTP_400_BAD_REQUEST)


# class ReviewViews(ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer


# api
class HomeViews(ModelViewSet):
    def list(self, request, *args, **kwargs):
        hotel_data = Hotel.objects.all()
        scenic_spot_data = ScenicSpot.objects.all()
        product_data = Product.objects.all()

        hotel_serializer = HotelSerializer(hotel_data, many=True)
        scenic_spot_serializer = ScenicSpotSerializer(scenic_spot_data, many=True)
        product_serializer = ProductSerializer(product_data, many=True)

        response_data = {
            'hotels': hotel_serializer.data,
            'scenic_spots': scenic_spot_serializer.data,
            'products': product_serializer.data,
        }

        return Response(response_data)


class allOrderViews(ModelViewSet):
    queryset = ScenicSpotOrder.objects.all()
    serializer_class = ScenicSpotOrderSerializer

    def list(self, request, *args, **kwargs):
        username = request.query_params.get('username', '').strip()
        if username:
            scenic_spot_orders = ScenicSpotOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'ScenicSpot__name', 'quantity', 'total_price', 'order_date', 'status')
            format_datetime(scenic_spot_orders)
            hotel_orders = HotelOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'hotel__name', 'quantity', 'total_price', 'order_date', 'status')
            format_datetime(hotel_orders)
            product_orders = ProductOrder.objects.filter(user__username__icontains=username) \
                .values('id', 'user__username', 'product__name', 'quantity', 'total_price', 'order_date', "status")
            format_datetime(product_orders)
            all_orders = list(chain(scenic_spot_orders, hotel_orders, product_orders))

            paid_orders = [order for order in all_orders if order['status'] == "已支付"]
            cancelled_orders = [order for order in all_orders if order['status'] == "已取消"]

            data = {
                "all_orders": all_orders,
                "paid_orders": paid_orders,
                "cancelled_orders": cancelled_orders
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please provide a username parameter"}, status=status.HTTP_400_BAD_REQUEST)
