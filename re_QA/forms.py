from django import forms 
from .models import Topic,TopicReply,QuestionUser,AnswerUser,AnswerUserProfile
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
        
    def save(self):
        topic_reply = super(TopicReplyForm, self).save(commit=True)
        user =  topic_reply.topic.user

        # 質問者のメールアドレスを見てメール送信
        question_user = QuestionUser.objects.filter(user=user).first()
        if question_user and question_user.email_notification:
            from django.core.mail import send_mail
            from config.settings import EMAIL_HOST_USER
            send_mail(
                '回答がありました',
                topic_reply.comment,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        return topic_reply

class QuestionUserForm(forms.ModelForm):
    
    class Meta:
        model   = QuestionUser
        fields  = [ "user","resident_area","resident_style"]

class AnswerUserForm(forms.ModelForm):
    
    class Meta:
        model   = AnswerUser
        fields  = [ "user","company" ]
        
class AnswerUserProfileForm(forms.ModelForm):

    class Meta:
        model   = AnswerUserProfile
        fields  = [ "user", "nickname" ]

class PhotoListForm(forms.ModelForm):

    class Meta:
        model   = PhotoList
        fields  = ['photo']

class DocumentListForm(forms.ModelForm):

    class Meta:
        model   = DocumentList
        fields  = ['document']