from rest_framework import serializers

# 因为有model  所以用modelSerializer
from goods.models import SKU


class HotSKUListSerializer(serializers.ModelSerializer):

    class Meta:

        model = SKU

        fields = ('id', 'name', 'price', 'default_image_url', 'comments')



# 搜索建立的序列化起
from .search_indexes import SKUIndex
from drf_haystack.serializers import HaystackSerializer

class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    class Meta:
        index_classes = [SKUIndex]

        fields = ('text', 'id', 'name', 'price', 'default_image_url', 'comments')