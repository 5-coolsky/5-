import re

from django.contrib.auth.backends import ModelBackend

from users.models import User

#  用户注册完 自动登录  自动将token 用户名和密码返回给前段
def jwt_response_payload_handler(token, user=None, request=None):
    #token,   jwt 生成的token
    # user=None,  jwt 验证成功之后的user
    # request=None  请求
    return {
        'token': token,
        'user_id':user.id,
        'username':user.username
    }














"""
1. 定义一个方法,
2. 把要抽取的代码 复制过去.哪里有问题改哪里 没有的变量定义位参数
3. 验证
"""

# 抽取
def get_user_by_account(username):


    try:
        if re.match(r'1[3-9]\d{9}', username):
            # 手机号
            user = User.objects.get(mobile=username)
        else:
            # 用户名
            user = User.objects.get(username=username)
    except User.DoesNotExist:
            user = None
    return user


# # jwt 把用户名和密码给系统,让系统进行认证,认证成功之后jwt 生成token 系统认证不能满足已有需求重写
#  ModelBackend为系统封装的参数， 需要配置并重写
class UsernameMobleModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):


        # try:
        #     if re.match(r'',username):
        #         # 手机号
        #         user = User.objects.get(mobile=username)
        #     else:
        #         # 用户名
        #         user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #         user = None

        user = get_user_by_account(username)
        # 2. 验证码用户密码
        if user is not None and user.check_password(password):
            return user
        # 必须返回数据
        return None




# # 扩展的
# class MyBackend(object):
#     def authenticate(self, request, username=None, password=None):
#         user = get_user_by_account(username)
#         # 2. 验证码用户密码
#         if user is not None and user.check_password(password):
#             return user
#         # 必须返回数据
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None




