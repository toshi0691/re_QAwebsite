from django import forms 
from .models import Topic,TopicReply
from .models import PhotoList,DocumentList

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        
#バリデーション対象のフィールドfieldsに入れる
        fields  = [ "comment","genre","user" ]

class TopicReplyForm(forms.ModelForm):

    class Meta:
        model   = TopicReply
        fields  = [ "comment","name","topic" ]
'''
class RegisterUserForm(forms.ModelForm):
    
    class Meta:
        model   = RegisterUser
        fields  = [ "u_name","u_name_kana","home_style","home_area","u_mail_address","u_phone_number","u_password"]
'''
class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']