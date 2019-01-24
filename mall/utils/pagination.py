from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # 每页几个
    page_size = 2
    # 设置重命名
    page_size_query_param = 'page_size'
    # 最大分页页数
    max_page_size = 20