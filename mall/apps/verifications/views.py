from django.shortcuts import render

# Create your views here.
import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection

from libs.yuntongxun.sms import CCP
# from verifications.serializers import RegisterSmscodeSerializer
from verifications.serializers import RegisterSmscodeSerializer

"""
1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.请求方式 路由
4.确定视图
5.按照步骤实现功能


图片验证码思路：

# 1.接受前段发送过来的image_code_id
# 2.生成验证码和图片
# 3.同时将验证码内容保存在redis中
# 4.返回响应

"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#ListAPIVIew,RetriveAPIView     封装好了

# 定义一个类
class RegisterImageAPIView(APIView):
    def get(self,request,image_code_id):
# 1.接受前段发送过来的image_code_id     因为已经接受了 所以此步骤不用写
# 2.生成验证码和图片  通过第三方库captcha.generate_captcha
        text,image = captcha.generate_captcha()
        print(text)
# 3.同时将验证码内容保存在redis中
# 3.1 连接redis
        redis_conn = get_redis_connection("code")
# 3.2  设置图片
        redis_conn.setex("img_"+image_code_id,5*60,text)
# 4.返回响应
        return HttpResponse(image,content_type="image/ipeg")

"""
1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.请求方式 路由
4.确定视图
5.按照步骤实现功能


手机短信验证码思路：

# 1.接收所有数据
# 2.校验
# 3.生成短信验证码
# 3.将短信验证码内容保存在redis中
# 4.使用云通讯发送短信
# 5.返回


"""
# 定义一个类  并在同文件夹下配置序列化器
class RegisterSmscodeAPIView(APIView):
    def get(self,request,mobile):
# 1.接受所有数据
        params = request.query_params

# 2.校验
        serializer = RegisterSmscodeSerializer(data=params)
        serializer.is_valid(raise_exception=True)
# 3.生成短信验证码
        sms_code = '%06d'%random.randint(0,999999)
        print(sms_code)
# 4.将短信验证码内容保存在redis中
        redis_conn = get_redis_connection('code')

        redis_conn.setex('sms_'+mobile,60,sms_code)
# 5.使用云通讯发送短信
#         CCP().send_template_sms(mobile,[sms_code,5],1)
        from clery_tasks.sms.tasks import send_sms_code

        # delay 的参数和 任务的参数对应
        # 必须调用 delay 方法  才能到broker中
        send_sms_code.delay(mobile, sms_code)
# 6.返回


        return Response({'msg':'ok'})


















