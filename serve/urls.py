from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', include('app.url')),
    path('api/', include('app.urls')),
    # path('app01/<int:id>/', include('app01.url')),
    # path('app02/', include('app02.url')),
    # 添加drf登录认证 -rest_framework.urls里面封装了登录和登出的视图
    path('api-auth/', include('rest_framework.urls')),
    # 接口自动生成接口文档
    re_path(r'^docs/', include_docs_urls(title='接口文档'))
]

