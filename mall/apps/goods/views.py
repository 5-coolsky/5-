from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from goods.models import SKU
from goods.serializers import HotSKUListSerializer
"""
表的设计 思想:
    1. 根据产品给的原型 尽量多的分析表的字段 (不要分析表和表之间的关系)
    2. 在一个安静的没有人打扰的环境中 分析表和表之间的关系(2个表和2个表去分析)
"""




"""
页面静态化  -- 提升用户体验 ,SEO

其实就是我们先把数据 查询出来,查询出来之后,将数据填充到模板中,
形式了html,将html写入到指定的文件

当用户访问的时候 ,直接访问 静态html


"""





'''
列表数据

热销列表  和普通列表展示

热销列表： 搜索那个产品的id 就展示哪个产品的热销数据

1.接受分类产品的id
2.根据id获取数据， 【SKU,SKU,SKU】
3.将数据转换成json
4.返回

GET      /goods/categories/(?P<category_id>\d+)/hotskus/
         /goods/categories/115/hotskus/

'''
class HotSKUListAPIView(ListAPIView):

    pagination_class = None

    # 因为是接受分类的产品 ，所以需要路由 搜索产品的category_id  而不是接受所有的数据
    # 由于不知道category_id去哪了   all属性看不到数据变化 所以需要self，只有重写才能得到self
    # queryset = SKU.objects.all()
    # ListAPIView 继承二级视图GenericAPIView  GenericAPIView的两个参数 重写get_queryset 和 get_serializer_class
    def get_queryset(self):

        category_id = self.kwargs["category_id"]

        return SKU.objects.filter(category_id=category_id).order_by('-sales')[:2]


    serializer_class = HotSKUListSerializer

"""
列表数据获取：
获取分类的数据 进行排序  再进行分页

先获取所有的数据
1.后端获取所有的数据
2.转换成json
3.返回


排序

分页

GET     /goods/categories/(?P<category_id>\d+)/skus/
"""

# 路由？page=3&ordering=price
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
# 两种分类形式   勿忘在setting中设置分页
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.generics import GenericAPIView  # 二级视图里面自带分类

class SKUListAPIView(ListAPIView):


    serializer_class = HotSKUListSerializer

    # queryset = SKU.objects.all()

    # 分页
    # pagination_class =

    def get_queryset(self):

        category_id = self.kwargs["category_id"]

        return SKU.objects.filter(category_id=category_id)

    # 排序
    filter_backends = [OrderingFilter]

    ordering_fields = ['create_time','sales','price']




#  搜索试图函数
from .serializers import SKUIndexSerializer
from drf_haystack.viewsets import HaystackViewSet
#                       一个类似于三级视图 搜索用的视图集   用了视图集 所以得重写路由
class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer

