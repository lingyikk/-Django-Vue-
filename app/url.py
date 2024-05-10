from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

# drf给url添加后缀
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

urlpatterns = [
    path('admin/User/search', views.UserViews.as_view({'get': 'search_user'}), name='user-search'),
    path('admin/User/login/', views.UserViews.as_view({'post': 'login'}), name='login'),
    path('admin/User/register/', views.UserViews.as_view({'post': 'register'}), name='register'),
    path('admin/admin/login/', views.adminViews.as_view({'post': 'login'}), name='login'),
    path('admin/admin/register/', views.adminViews.as_view({'post': 'register'}), name='register'),
    path('admin/Hotel/search/', views.HotelViews.as_view({'get': 'search_hotel'}), name='hotel-search'),
    path('admin/ScenicSpot/search/', views.ScenicSpotViews.as_view({'get': 'search_ScenicSpot'}), name='ScenicSpot-search'),
    path('admin/product/search/', views.ProductViews.as_view({'get': 'search_product'}), name='product-search'),
    path('admin/ScenicSpotOrder/search/', views.ScenicSpotOrderViews.as_view({'get': 'search_ScenicSpotOrder'}), name='ScenicSpotOrder-search'),
    path('admin/HotelOrder/search/', views.HotelOrderViews.as_view({'get': 'search_HotelOrder'}), name='HotelOrder-search'),
    path('admin/ProductOrder/search/', views.ProductOrderViews.as_view({'get': 'search_ProductOrder'}), name='ProductOrder-search'),
    # path('admin/allOrder/', views.allOrderViews.as_view({'get': 'list'}), name='allOrder'),
    # path('login', TokenObtainPairView.as_view(), name='login'),  # 登录
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  # token刷新
    # path('token/verify', TokenVerifyView.as_view(), name='token_verify'),   # token校验
]

# DRF中的路由注册，只支持视图集中使用
router = routers.SimpleRouter()
router.register('User', views.UserViews)
router.register('admin', views.adminViews)
router.register('ScenicSpot', views.ScenicSpotViews)
router.register('Hotel', views.HotelViews)
router.register('product', views.ProductViews)
# router.register('Review', views.ReviewViews)
router.register('ScenicSpotOrder', views.ScenicSpotOrderViews)
router.register('ProductOrder', views.ProductOrderViews)
router.register('HotelOrder', views.HotelOrderViews)
router.register('allOrder', views.allOrderViews)


# router.register('addr', views.AddrViews)
# router.register('file', views.FileViews)
urlpatterns += router.urls


# 7、视图中原生的写法:
# urlpatterns = [
#     path('users/', views.UserViews.as_view({'get': 'list', 'post': 'create'})),
#     path('users/<int:pk>/', views.UserViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
# ]


# 3-6、基于APIView对视图函数进行重构
# urlpatterns = [
#     path('users/', views.UserListViews.as_view()),
#     path('users/<int:id>/', views.UserDeleteViews.as_view()),
# ]

# 1-2、
# urlpatterns = [
#     path('users/', views.user_list),
#     path('users/<int:id>/', views.user_detail),
# ]

urlpatterns = format_suffix_patterns(urlpatterns)

