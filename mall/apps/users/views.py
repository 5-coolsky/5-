from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import mixins
from rest_framework.response import Response

# from mall.apps.users.models import User
# from apps.users.models import User
# from users.models import User   setting 里面设置过 默认从 apps里面找  所以就不用加apps的前缀了
# 正确
from rest_framework.viewsets import GenericViewSet

from goods.models import SKU
from users.models import User
from users.serialziers import RegiserUserSerializer, UserCenterInfoSerializer, UserEmailInfoSerializer, \
    AddressSerializer, AddUserBrowsingHistorySerializer, SKUSerializer, AddressTitleSerializer
from users.utils import check_token

"""
 前端发送用户给后端 我们后端判断用户名 是否注册

 请求方式:
 GET        /users/usernames/(?P<username>\w{5,20})/count/

 # itcast 0
 # itcast 1

 POST


"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#ListAPIVIew,RetriveAPIView     封装好了
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
class RegisterUsernameAPIView(APIView):


    def get(self,request,username):

        count = User.objects.filter(username=username).count()


        return Response({
            "count":count,
            "username":username
        })     #  postman里面去验证


# 定义手机号

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import User
# # Create your views here.
#
# class RegisterPhoneCountAPIView(APIView):
#     """
#     查询手机号的个数
#     GET: /users/phones/(?P<mobile>1[345789]\d{9})/count/
#     """
#     def get(self,request,mobile):
#
#         #通过模型查询获取手机号个数
#         count = User.objects.filter(mobile=mobile).count()
#         #组织数据
#         context = {
#             'count':count,
#             'phone':mobile
#         }
#
#         return Response(context)


"""

1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.路由和请求方式
4.确定视图
5.按照步骤实现功能

当用户点击注册按钮的时候 前端需要收集     手机号,用户名,密码,短信验证码,确认密码,是否同意协议

1. 接收数据
2. 校验数据
3. 数据入库
4. 返回相应

POST    /users/register/



"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#CreateAPIView                  封装好了

class RegiserUserAPIView(APIView):

    def post(self,reqeust):
        # 1. 接收数据
        data = reqeust.data
        # 2. 校验数据
        serializer = RegiserUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. 数据入库
        serializer.save()
        # 4. 返回相应
        return Response(serializer.data)


"""
当用户注册成功之后,自动登陆

自动登陆的功能 是要求 用户注册成功之后,返回数据的时候
需要额外添加一个 token

1. 序列化的时候 添加token
2. token 怎么生成

"""







####  第五天
"""
个人中心 信息展示，必须是登陆用户才能访问

1.前段发送get请求，后端接受数据
2.根据用户的信息获取user
3.将对象转换成字典数据
4.返回

GET     /users/infos/
"""

# 个人中心 一级视图写法
# from rest_framework.permissions import IsAuthenticated
# class UserCenterInfoAPIView(APIView):
#     # 添加用户权限 只有登陆的才能访问
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
# # 1.前段发送get请求，后端接受数据 获取user 因为HttpRequest中
# # user可以直接获取用户信息，所以
#         user = request.user
# # 2.将模型转换成JSON（字典格式）
#         serializer = UserCenterInfoSerializer(user)
#
# # 3.返回
#         return Response(serializer.data)

# 个人中心  三级视图写法
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
class UserCenterInfoAPIView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserCenterInfoSerializer

    # queryset = User.objects.all()
    # RetrieveAPIView里面的RetrieveModelMixin里面的instance = self.get_object()不能满足，需要重写
    def get_object(self):

        return self.request.user

"""
当用户输入 邮箱 点击保存的时候
1.后端需要接受数据并将其保存在mysql  email字段
2.同时后端需要将给邮箱发送一个激活连接
3.用户进入邮箱点击激活


代码步骤：
1.后端需要接受邮箱
2.校验
3.更新保存数据
4.返回响应

PUT     /users/emails/

"""

# # 个人中心邮箱 一级视图写法
# from rest_framework.permissions import IsAuthenticated
# class UserEmailInfoAPIView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def put(self,request):
#
#     # 1.后端需要接受邮箱
#         data = request.data
#     # 2.校验
#         serializer = UserEmailInfoSerializer(instance=request.user, data=data)
#         serializer.is_valid(raise_exception=True)
#             # 3. 更新数据
#         serializer.save()
#              # 发送邮件
#             # 4. 返回相应
#         return Response(serializer.data)


# 个人中心 三级视图写法
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
class UserEmailInfoAPIView(UpdateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserEmailInfoSerializer

    def get_object(self):

        return self.request.user

"""
激活需求：
1.用户在邮箱里面点击连接 激活 传给前段一个带token 的信息
2.然后前段将这个信息请求发送给后端



1.后端接受数据
2.对token解析
3.获取user_id 进行查询
4.修改状态
5.返回响应

GET     /users/emails/verification/

"""

# 用虚拟机浏览器验证
from rest_framework import status
class UserEmailVerificationAPIView(APIView):

    def get(self,request):
        # 1. 接收token信息
        token = request.query_params.get('token')
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 2. 对token进行解析
        user_id = check_token(token)


        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 3. 解析获取user_id之后,进行查询
        user = User.objects.get(pk=user_id)
        # 4. 修改状态
        user.email_active=True
        user.save()
        # 5. 返回相应
        return Response({'msg':'ok'})



"""
1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.路由和请求方式
4.确定视图
5.按照步骤实现功能

新增地址

1. 后端接收数据
2. 对数据进行校验
3. 数据入库
4. 返回相应

POST        /users/addresses/

"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#CreateAPIView                   封装好了

# from rest_framework.generics import CreateAPIView
# from rest_framework.generics import GenericAPIView
#
# #GenericAPIView 下面的 Generics  搜索context 点击后面的get_serializer_context  有request,formate,view
#
# class UserAddressAPIView(CreateAPIView):
#
#     permission_classes = [IsAuthenticated]
#
#     serializer_class = AddressSerializer
#
#     # queryset =  新增数据用不到该属性

class AddressViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,GenericViewSet):
    """
    用户地址新增与修改
    list GET: /users/addresses/
    create POST: /users/addresses/
    destroy DELETE: /users/addresses/
    action PUT: /users/addresses/pk/status/
    action PUT: /users/addresses/pk/title/
    """

    #制定序列化器
    serializer_class = AddressSerializer
    #添加用户权限
    permission_classes = [IsAuthenticated]
    #由于用户的地址有存在删除的状态,所以我们需要对数据进行筛选
    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        count = request.user.addresses.count()
        if count >= 20:
            return Response({'message':'保存地址数量已经达到上限'},status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)

    def list(self, request, *args, **kwargs):
        """
        获取用户地址列表
        """
        # 获取所有地址
        queryset = self.get_queryset()
        # 创建序列化器
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        # 响应
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 20,
            'addresses': serializer.data,
        })

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.decorators import action


@action(methods=['put'], detail=True)
def title(self, request, pk=None, address_id=None):
    """
    修改标题
    """
    address = self.get_object()
    serializer = AddressTitleSerializer(instance=address, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)



"""

最近浏览记录
1. 必须是登陆用户的 我们才记录浏览记录
2. 在详情页面中添加 , 添加商品id 和用户id
3. 把数据保存在数据库中是每问题的
4. 我们把数据保存在redis的列表中 (回顾redis)


"""

"""
添加浏览记录的业务逻辑

1. 接收商品id
2. 校验数据
3. 数据保存到redis中
4. 返回相应

post    /users/histories/
"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#CreateAPIView                   封装好了
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
class UserHistoryAPIView(CreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = AddUserBrowsingHistorySerializer


    """

    获取浏览记录数据

    1. 从redis中获取数据   [1,2,3]
    2. 根据id查询数据     [SKU,SKU,SKU]
    3. 使用序列化器转换数据
    4. 返回相应

    GET
    """
    def get(self,request):

        user = request.user

    # 1.连接redis

        redis_conn = get_redis_connection("history")

        ids = redis_conn.lrange("history_%s" %user.id,0,4)
    # 2.读取查询浏览数据
        skus = []
        for id in ids:

            sku = SKU.objects.get(pk=id)
            skus.append(sku)
    # 3.使用序列化转换数据
        serializer = SKUSerializer(instance = skus,many = True)

        return Response(serializer.data)


# 购物车合并的时候，需要用户登陆才能合并，但是用户登录跳转的时候urls用的是:url(r'^auths/',obtain_jwt_token),
# obtain_jwt_token 里面没有封装着合并的步骤，不能满足。所以得需要在子应用user中重写
from rest_framework_jwt.views import ObtainJSONWebToken
from carts.utils import merge_cookie_to_redis
class MergeLoginAPIView(ObtainJSONWebToken):


    def post(self, request, *args, **kwargs):
        # 调用jwt扩展的方法，对用户登录的数据进行验证
        response = super().post(request)

        # 如果用户登录成功，进行购物车数据合并
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 表示用户登录成功
            user = serializer.validated_data.get("user")
            # 合并购物车
            # merge_cart_cookie_to_redis(request, user, response)
            response = merge_cookie_to_redis(request, user, response)

        return response