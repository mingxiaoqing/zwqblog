#此文件名不可更改，表示在该app下全文检索
from haystack import indexes
from .models import Article

#创建类ArticleIndex 代表会对Article模型进行全文检索
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()