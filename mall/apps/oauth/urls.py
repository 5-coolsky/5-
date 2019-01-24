from django.conf.urls import url
from .views import OAuthQQURLAPIView,OAuthQQUserAPIView
urlpatterns =[
    # QQ跳转时的路由
    url(r'^qq/statues/$',OAuthQQURLAPIView.as_view()),

# code换token的路由
    url(r'^qq/users/$',OAuthQQUserAPIView.as_view()),
]