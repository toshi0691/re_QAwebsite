from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):

    name    = models.CharField(verbose_name="投稿者の名前",max_length=100,default="匿名")
    comment     = models.CharField(verbose_name="コメント",max_length=2000)
    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    
    def __str__(self):
        return self.comment
    
class PhotoList(models.Model):

    photo       = models.ImageField(verbose_name="フォト",upload_to="file/photo_list/photo/")
    
class DocumentList(models.Model):

    document    = models.FileField(verbose_name="ファイル",upload_to="file/document_list/document/")
    

    
#質問者会員登録
#回答者会員登録
#回答者のプロフィール作成
