from django import forms 
from .models import Topic
from .models import PhotoList,DocumentList

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "comment" ]

class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']