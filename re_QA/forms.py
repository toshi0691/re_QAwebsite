from django import forms 
from .models import Topic,TopicReply,QuestionUser,AnswerUser
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

class QuestionUserForm(forms.ModelForm):
    
    class Meta:
        model   = QuestionUser
        fields  = [ "user","resident_area","resident_style"]

class AnswerUserForm(forms.ModelForm):
    
    class Meta:
        model   = AnswerUser
        fields  = [ "user","company" ]

class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']