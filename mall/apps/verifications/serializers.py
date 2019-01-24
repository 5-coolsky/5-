from rest_framework import serializers
from django_redis import get_redis_connection
# ModelSerializer 确实可以自动生成字段,也有 create和update方法
# 但是 必须有 Model


class RegisterSmscodeSerializer(serializers.Serializer):
    # 用户输入的验证码
    text = serializers.CharField(max_length=4, min_length=4, required=True)
    #  redis的UUid
    image_code_id = serializers.UUIDField(required=True)

    """
    序列化的验证:
    1. 字段类型
    2. 字段选项
    3. 单个字段
    4. 多个字段
    """
    #  由于接受text和image_code_id   所以用多数据校验
    def validate(self, attrs):

        # 1.获取用户提交的验证码
        text = attrs.get("text")
        # 2.获取redis的验证码
        # 2.1 连接redis
        redis_conn = get_redis_connection("code")
        # 2.2  获取数据
        image_id = attrs.get("image_code_id")

        redis_text = redis_conn.get("img_"+str(image_id))

        # 2.3 redis的数据有时效性 验证时间
        if redis_text is None:
            raise serializers.ValidationError("图片验证码过期")

        # 3 比对   decode（）解码    lower 是大小写转换
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('输入错误')

        return attrs


