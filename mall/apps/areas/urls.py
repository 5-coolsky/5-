#  注册路由
from django.conf.urls import url

from .views import  AreaModelViewSet


urlpatterns = [
]

# 1.导入Router

from rest_framework.routers import DefaultRouter

# 2.创建Router实力对象
router = DefaultRouter()

# 3.注册路由
#                 路由      视图级
router.register(r'infos',AreaModelViewSet,base_name='area')

#4.添加到 urlpatterns

urlpatterns += router.urls