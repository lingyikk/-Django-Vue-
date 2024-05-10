from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

# drf给url添加后缀
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

urlpatterns = [
    # path('admin/User/search', views.UserViews.as_view({'get': 'search_user'}), name='user-search'),
    # path('admin/User/login/', views.UserViews.as_view({'post': 'login'}), name='login'),
    # path('admin/User/register/', views.UserViews.as_view({'post': 'register'}), name='register'),
    # path('admin/Hotel/search/', views.HotelViews.as_view({'get': 'search_hotel'}), name='hotel-search'),
]

# DRF中的路由注册，只支持视图集中使用
router = routers.SimpleRouter()
router.register('home', views.HomeViews, basename='home')

# router.register('User', views.UserViews)
# router.register('ScenicSpot', views.ScenicSpotViews)
# router.register('Hotel', views.HotelViews)
# router.register('product', views.ProductViews)
# # router.register('Review', views.ReviewViews)
# router.register('ScenicSpotOrder', views.ScenicSpotOrderViews)
# router.register('ProductOrder', views.ProductOrderViews)
# router.register('HotelOrder', views.HotelOrderViews)
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)

