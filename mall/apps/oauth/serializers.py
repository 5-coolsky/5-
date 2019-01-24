# serializers.Serializer

# 因为model中字段较少，添加麻烦，所以用serializer
# serializers.ModelSerializer
from rest_framework import serializers


from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.utils import check_access_token
from users.models import User
from .models import OAuthQQUser
# serializers.Serializer
# serializers.ModelSerializer

"""
手机号,密码,短信验证码和加密的openid 这些数据进行校验

校验没有问题 保存数据的时候 是保存的 user 和openid

"""
class OAuthQQUserSerializer(serializers.Serializer):

    access_token = serializers.CharField(label='操作凭证')  # 指openid字段
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    # 需要验证，因为不是一个字段，所以得用多字段验证
    def validate(self, attrs):

        # 1.对openid进行验证
        # 获取字段里面的openid
        access_token = attrs.get("access_token")

        openid = check_access_token(access_token)
        # 判断openid
        if openid is None:

            raise serializers.ValidationError("openid错误")
        # 通过attrs来传递数据
        attrs["openid"] = openid


        #2. 需要对短信进行验证
        # 2.1 获取用户提交的
        mobile = attrs.get('mobile')
        sms_code = attrs['sms_code']
        # 2.2 获取 redis
        redis_conn = get_redis_connection('code')

        redis_code = redis_conn.get('sms_' + mobile)

        if redis_code is None:
            raise serializers.ValidationError('短信验证码已过期')

        # 最好删除短信
        redis_conn.delete('sms_' + mobile)
        # 2.3 比对
        if redis_code.decode() != sms_code:
            raise serializers.ValidationError('验证码不一致')

        #3. 需要对手机号进行判断
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            #说明没有注册过
            #创建用户
            # User.objects.create()
            pass
        else:
            #说明注册过,
            # 注册过需要验证密码
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('密码不正确')

            attrs['user']=user


        return attrs


# serializer.Serializer的序列化器去调用views中的save方法的时候需要在序列化器里面手动
# 填写create方法

    # request.data --> 序列化器(data=xxx)
    # data --> attrs -->validated_data
    def create(self, validated_data):

        user = validated_data.get('user')

        if user is None:
            #创建user
            user = User.objects.create(
                mobile=validated_data.get('mobile'),
                username=validated_data.get('mobile'),
                password=validated_data.get('password')
            )

            #对password进行加密
            user.set_password(validated_data['password'])
            user.save()

        qquser = OAuthQQUser.objects.create(
            user=user,
            openid=validated_data.get('openid')
        )


        return qquser














