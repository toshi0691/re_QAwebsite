from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):

    name     = models.CharField(verbose_name="投稿者の名前",max_length=100,default="匿名")
    comment  = models.CharField(verbose_name="コメント",max_length=2000)
    dt       = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    genre    = models.CharField(verbose_name="質問のジャンル",max_length=20)
    
    def __str__(self):
        return self.comment
    
class TopicReply(models.Model):
    topic    = models.ForeignKey(Topic,verbose_name="対象トピック",on_delete=models.CASCADE)
    
    name     = models.CharField(verbose_name="投稿者の名前",max_length=100,default="匿名")
    comment  = models.CharField(verbose_name="コメント",max_length=2000)
    dt       = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    

    

    
class PhotoList(models.Model):
    photo       = models.ImageField(verbose_name="フォト",upload_to="file/photo_list/photo/")
    
class DocumentList(models.Model):
    document    = models.FileField(verbose_name="ファイル",upload_to="file/document_list/document/")


#質問者会員登録
#class RegiUser(models.Model):
    
#    u_name    = models.CharField(verbose_name="会員登録ユーザーの名前",max_length=30)
#    home_style     = models.CharField(verbose_name="会員登録ユーザーの居住スタイル",max_length=30)
#    home_area     =  models.CharField(verbose_name="会員登録ユーザーの居住エリア",max_length=30)
#    u_mail_address     = models.CharField(verbose_name="会員登録ユーザーのメールアドレス",max_length=70)
#    u_phone_number     = models.IntegerField(verbose_name="会員登録ユーザーの電話番号",max_length=11)
#    u_password     = models.CharField(verbose_name="会員登録ユーザーの名前",min_length=8,max_length=20)



#回答者会員登録
#class RegiAnswerer(models.Model):
    
#    a_name     = models.CharField(verbose_name="会員登録回答者の名前",max_length=30)
#    a_mail_address     = models.CharField(verbose_name="会員登録回答者のメールアドレス",max_length=70)
#    a_phone_number     = models.IntegerField(verbose_name="会員登録回答者の電話番号",max_length=11)





#回答者のプロフィール作成
