from haystack import indexes

from .models import SKU

        #  SearchIndex   必备的参数       必备的参数
class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    """
    # 每个SearchIndex必须得有一个字段是document=True     text可以是任意字母，但是一般用text接受  可以理解为索引页
    text = indexes.CharField(document=True, use_template=True)   # 表示可以指定字段去搜索
    # 搜索要展示的东西
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.CharField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')
    # index继承里面有这两个参数方法
    def get_model(self):
        """返回建立索引的模型类   也就是查询哪个模型里面的数据"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集  也就是吧所有的数据返回去"""
        return self.get_model().objects.filter(is_launched=True)

    #   在模板中创建 templates就是模板类文件夹 search/indexes/myapp/note_rendered.txt
    #   search/indexes 不能变    myapp指商品的文件 这里是goods    note_rendered.txt指你要查询的模型类，这里是sku_text.txt
