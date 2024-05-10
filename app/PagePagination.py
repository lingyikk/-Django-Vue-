from rest_framework.pagination import PageNumberPagination


# 自定义用户信息分页器
class UserPagination(PageNumberPagination):
    # 默认每页数据量
    page_size = 10
    # 前端发送的页数关键字名，默认为"page"
    page_query_param = 'page'
    # 前端发送的每页数目关键字名，默认为None -> 可以get传参设置一页多少个数据，不写就默认page__size个
    page_size_query_param = 'size'
    # 前端最多能设置的每页数量
    max_page_size = 10

# http://127.0.0.1:8010/app01/users/?page=1&size=4
















