from django.conf.urls import url
from . import views

urlpatterns = [

    #/goods/categories/(?P<category_id>\d+)/hotskus/
    # 热销
    url(r'^categories/(?P<category_id>\d+)/hotskus/$',views.HotSKUListAPIView.as_view(),name='hot'),
    #分类列表所有数据 详情，排序 分页
    url(r'^categories/(?P<category_id>\d+)/skus/$',views.SKUListAPIView.as_view(),name='hot'),

]

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='skus_search')

urlpatterns += router.urls