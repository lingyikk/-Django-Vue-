# from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户类
class User(models.Model):
    username = models.CharField("游客名称", max_length=150, unique=True)
    password = models.CharField("密码", max_length=20, default=123123)
    email = models.EmailField("邮箱", unique=True, blank=True, null=True)
    phone_number = models.CharField("手机号码", max_length=15, blank=True, null=True)
    registration_date = models.DateTimeField("注册时间", auto_now_add=True)

    # USER_TYPE_CHOICES = [
    #     ('guest', '游客'),
    #     ('hotel_manager', '酒店管理'),
    #     ('scenic_spot_manager', '景点管理'),
    #     ('admin', '管理员'),
    # ]
    # user_type = models.CharField("用户类型", max_length=20, choices=USER_TYPE_CHOICES, default='guest')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "游客"
        verbose_name_plural = "游客"


# class Role(models.Model):
#     name = models.CharField("角色名称", max_length=100)
#     description = models.TextField("角色描述")
#
#     def __str__(self):
#         return self.name
#
#
# class Permission(models.Model):
#     name = models.CharField("权限名称", max_length=100)
#     description = models.TextField("权限描述")
#
#     def __str__(self):
#         return self.name
#
#
# class UserRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#
#
# class RolePermission(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

# 管理员
class admin(models.Model):
    username = models.CharField("管理员名称", max_length=150, unique=True)
    password = models.CharField("密码", max_length=20, default=123123)
    registration_date = models.DateTimeField("注册时间", auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = "管理员"


# 景点类
class ScenicSpot(models.Model):
    name = models.CharField(max_length=100, verbose_name='景点名称', default=None)
    description = models.TextField(verbose_name='景点描述', default=None)
    city = models.CharField(max_length=50, verbose_name='所在城市', default=None)
    location = models.CharField(max_length=200, verbose_name='具体地址', default=None)
    open_hours = models.CharField(max_length=100, verbose_name='开放时间', default=None)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='门票价格', default=None)
    star = models.IntegerField(verbose_name='景点级别', default=None)
    stock = models.IntegerField(verbose_name='余票', default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '景点'
        verbose_name_plural = '景点'


# 酒店类
class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name='酒店名称')
    city = models.CharField(max_length=50, verbose_name='所在城市')
    addr = models.CharField(max_length=200, verbose_name='具体地址')
    detail = models.TextField(verbose_name='酒店描述')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(verbose_name='剩余房间数')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "酒店"
        verbose_name_plural = "酒店"


# 商品类
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='产品名称', unique=True)
    detail = models.TextField(verbose_name='产品描述')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    type = models.CharField(max_length=100, verbose_name='类型')
    sales = models.PositiveIntegerField(verbose_name='销量')
    stock = models.PositiveIntegerField(verbose_name='库存')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"


# # # # 评论类
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField("评论内容")
    date = models.DateTimeField("评论时间", auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"


# 景区订单类
class ScenicSpotOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    ScenicSpot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name="景区")
    quantity = models.PositiveIntegerField("数量", default=1)
    total_price = models.DecimalField("总价", max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, verbose_name='状态', default="已取消")
    order_date = models.DateTimeField("下单时间", auto_now_add=True)

    class Meta:
        verbose_name = "景区订单"
        verbose_name_plural = "景区订单"


# 酒店订单类
class HotelOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name="酒店")
    quantity = models.PositiveIntegerField("数量", default=1)
    total_price = models.DecimalField("总价", max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, verbose_name='状态', default="已取消")
    order_date = models.DateTimeField("下单时间", auto_now_add=True)

    class Meta:
        verbose_name = "酒店订单"
        verbose_name_plural = "酒店订单"


# 产品订单类
class ProductOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField("数量", default=1)
    total_price = models.DecimalField("总价", max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, verbose_name='状态', default="已取消")
    order_date = models.DateTimeField("下单时间", auto_now_add=True)

    class Meta:
        verbose_name = "产品订单"
        verbose_name_plural = "产品订单"
