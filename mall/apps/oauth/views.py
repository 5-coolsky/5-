from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from mall import settings
from rest_framework import status

from oauth.models import OAuthQQUser
# from oauth.serializers import OAuthQQUserSerializer
# from oauth.utils import generic_open_id
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import generic_open_id

'''
1.当我们点击QQ登陆的时候，返回给前段一个url，也就是
QQ登陆绑定页面 ，所以应该去设置这个视图函数

'''

class OAuthQQURLAPIView(APIView):

    def get(self,request):

        # status 代表登陆之后跳转到哪里  “/”代表跳转到首页
        state = '/'
        # 1.创建oauth的实例化对象
        # 1.1   OAuthQQ 是封装好的函数，三个为参数  state没有固定要求，先随便定义一个参数
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)

        # 2.获取需要跳转的url
        # 前段写的是auth_url
        auth_url = oauth.get_qq_url()

        return Response({"auth_url":auth_url})


"""
1.用户扫描二维码或者登陆同意的时候，后端会返回给前段一个code
2.前段需要拿着这个code去换token
3.前段换到token后继续换成openid



GET     /oauth/qq/users/?code=xxxxxx
"""

# 书写code换成token的流程
# 1.后端需要先接受前段发过来的code
class OAuthQQUserAPIView(APIView):

    def get(self,request):
        # 1. 接收这个数据
        params = request.query_params
        code = params.get("code")
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 2. 用code换token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        # code申请返回token的时候 state不是必须需要返回的，所以可以省略不写
        # 返回成功后，里面携带者access_token和get_access_token方法，所以
        token = oauth.get_access_token(code)
        print(token)
        # code:605B4C869E89EA4AC9B09D2B29852723
        # token:ADD4B8F798DC0C4A0D8D38FE5EB79CD8

        # 3. 用token换openid
        openid = oauth.get_open_id(token)

        # openid是此网站上唯一对应用户身份的标识，网站可将此ID进行存储便于用户下次登录时辨识其身份
        # 获取的openid有两种情况:
        # 1. 用户之前绑定过
        # 2. 用户之前没有绑定过
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在  需要绑定


            #  需要封装  在自应用oauth中建立utils封装

            # s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
            # # 2.组织数据
            # data = {
            #     'openid': openid
            # }
            # # 3. 让序列化器对数据进行处理
            # # dumps就是转化成字符串形式
            # token = s.dumps(data)


            #
            token = generic_open_id(openid)
            # 没有openid 得需要返回给前段登陆页面去绑定
            return Response({
                'access_token':token
            })

        else:
            # 存在 直接登陆  因为是登陆，所以只需要token不需要openid
            from rest_framework_jwt.settings import api_settings
            #这四部是拿取token的过程
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(qquser.user)
            token = jwt_encode_handler(payload)



            return Response({
                'token': token,
                'username': qquser.user.username,
                'user_id': qquser.user.id
            })

        # finally:

            # openid 很重要 ,所以我们需要对openid进行一个处理
            # 绑定也应该有一个时效





    """
    当用户点击绑定的时候 ,我们需要将 手机号,密码,短信验证码和加密的openid 传递过来

    1. 接收数据
    2. 对数据进行校验
    3. 保存数据
    4. 返回相应


    POST    /oauth/qq/users/

    """
    def post(self,request):

        # 1. 接收数据
        data = request.data
        # 2. 对数据进行校验
        serializer = OAuthQQUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. 保存数据
        qquser = serializer.save()
        # 4. 返回相应
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(qquser.user)
        token = jwt_encode_handler(payload)

        return Response({
            'token': token,
            'username': qquser.user.username,
            'user_id': qquser.user.id
        })












#  openid是比较机密的 所及得加密
# 1.导入模型  并创建一个序列化器
from mall import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#  BadSignature   SignatureExpired 是两个错误  SignatureExpired继承BadSignature
from itsdangerous import BadSignature,SignatureExpired
# 创建序列化器
## secret_key: 秘钥 也就是settings中的SECRET_KEY
## expires_in :停留时间
s = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
# 2.组织数据
data = {
    'openid':"1234567890"
}
# 3. 让序列化器对数据进行处理
# dumps就是转化成字符串形式
token = s.dumps(data)
# 字符串类型  形式是JWT
# b'eyJhbGciOiJIUzI1NiIsImV4cCI6MTU0NzEzOTcwNiwiaWF0IjoxNTQ3MTM2MTA2fQ.
# eyJvcGVuaWQiOiIxMjM0NTY3ODkwIn0.
# p-5rdSoxiXNbiVg8EukHxvl4PUyqFBIKqV-mgSamKZ4'


# 4.获取数据对数据进行解密
s.loads(token)