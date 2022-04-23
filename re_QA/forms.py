from django import forms 
from .models import Topic,TopicReply
from .models import PhotoList,DocumentList

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "comment","genre" ]

class TopicReplyForm(forms.ModelForm):

    class Meta:
        model   = TopicReply
        fields  = [ "comment","name","topic" ]

class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']