from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator

#from django.core.mail import send_mail

import uuid 
# Create your models here.
class AnswerUserProfile(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name="ユーザー", on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name="ペンネーム",max_length=30)
    points   = models.IntegerField(default=0)
    questions= models.IntegerField(default=0)
    answers  = models.IntegerField(default=0)
class Topic(models.Model):

    id       = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user     = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="ユーザー",on_delete=models.CASCADE)
    name     = models.CharField(verbose_name="投稿者の名前",max_length=100,default="匿名")
    comment  = models.CharField(verbose_name="コメント",max_length=2000)
    dt       = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    genre    = models.CharField(verbose_name="質問のジャンル",max_length=20)
    views    = models.IntegerField(default=0)
    answers  = models.IntegerField(default=0)
    answered = models.IntegerField(default=0)
    def one_week():
        return timezone.now() + timezone.timedelta(days=7)

    deadline    = models.DateTimeField( verbose_name="回答受付期限", default=one_week )


    def __str__(self):
        return self.comment
    
    #TODO:userモデルと1対多のリレーションを組む
    #TODO:この質問に対して寄せられた回答数をカウントするメソッド
    # def count_reply():
        
    #TODO:この質問に対して寄せられた回答を出力するメソッド
    #TODO:質問の期限が来たら回答を受け付けないようにする
    


    
#質問に対して、一次回答は回答者登録者のみでき、二次以降は誰でも回答可能に。


class QuestionUser(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name="ユーザー", on_delete=models.CASCADE)
    resident_area = models.CharField(verbose_name="質問者の居住エリア",max_length=30)
    resident_style = models.CharField(verbose_name="質問者の居住スタイル",max_length=30)
    email_notification = models.BooleanField(default=False)
    registration_time = models.DateTimeField(auto_now_add=True, blank=True)
    
    #(https://stackoverflow.com/questions/39883950/str-returned-non-string-type-tuple)
    # def __str__(self):
    #     template = '{0.resident_area}{0.resident_style}'
    #     return template.format(self)
    
class AnswerUser(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name="ユーザー", on_delete=models.CASCADE)
    company  = models.CharField(verbose_name="回答者の会社名",max_length=30)
    approval    = models.BooleanField(verbose_name="回答権利",default=False)
    registration_time = models.DateTimeField(auto_now_add=True, blank=True)
    count_commented = models.IntegerField(default=0)
    count_good = models.IntegerField(default=0)
    count_bad = models.IntegerField(default=0)
    
    # def __str__(self):
    #     return self.company
    
    
# class AnswerUserProfile(models.Model):
#     user     = models.OneToOneField(settings.AUTH_USER_MODEL,verbose_name="ユーザー", on_delete=models.CASCADE)
#     nickname = models.CharField(verbose_name="ペンネーム",max_length=30)
#     points   = models.IntegerField(default=0)
#     questions= models.IntegerField(default=0)
#     answers  = models.IntegerField(default=0)

class TopicReply(models.Model):
    topic    = models.ForeignKey(Topic,verbose_name="対象トピック",on_delete=models.CASCADE)
    user     = models.ForeignKey(AnswerUserProfile,on_delete=models.CASCADE)
    name     = models.CharField(verbose_name="投稿者の名前",max_length=100,default="匿名")
    comment  = models.CharField(verbose_name="コメント",max_length=2000)
    votes    = models.IntegerField(default=0)
    accepted = models.IntegerField(default=0)
    dt       = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

class Vote(models.Model):
	answer   = models.ForeignKey(TopicReply,on_delete=models.CASCADE)
	user     = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	vote     = models.IntegerField(default=0)
	def __str__(self):
		return self.answer

class ValidationCode(models.Model):
    code = models.CharField(verbose_name='登録用コード', max_length=30)
    purpose = models.CharField(verbose_name='使用目的', max_length=30)
    source = models.CharField(verbose_name='紹介方法', max_length=30)











    

    
class PhotoList(models.Model):
    photo       = models.ImageField(verbose_name="フォト",upload_to="file/photo_list/photo/")
    
class DocumentList(models.Model):
    document    = models.FileField(verbose_name="ファイル",upload_to="file/document_list/document/")


#質問者会員登録
'''
class RegisterUser(models.Model):
    
    u_name    = models.CharField(verbose_name="会員登録ユーザーの名前",max_length=30)
    u_name_kana   = models.CharField(verbose_name="会員登録ユーザーの名前",max_length=30)
    home_style     = models.CharField(verbose_name="会員登録ユーザーの居住スタイル",max_length=30)
    home_area     =  models.CharField(verbose_name="会員登録ユーザーの居住エリア",max_length=30)
    u_mail_address     = models.CharField(verbose_name="会員登録ユーザーのメールアドレス",max_length=70)
    ###長さ10桁までかも↓
    u_phone_number     = models.IntegerField(verbose_name="会員登録ユーザーの電話番号")
    u_password     = models.CharField(verbose_name="会員登録ユーザーの名前",max_length=20)
'''



    

#回答者会員登録
#class RegisterAnswerer(models.Model):
    
#    a_name     = models.CharField(verbose_name="会員登録回答者の名前",max_length=30)
#    a_mail_address     = models.CharField(verbose_name="会員登録回答者のメールアドレス",max_length=70)
#    a_phone_number     = models.IntegerField(verbose_name="会員登録回答者の電話番号",max_length=11)





#回答者のプロフィール作成
