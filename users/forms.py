from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from re_QA.forms import QuestionUserForm,AnswerUserForm

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ("username","u_last_name","u_first_name","u_last_name_kana","u_first_name_kana","email","phone_number")
        #

    #def signup(self, request, user):
    #    user.is_active = False
    #    user.save()
    
    #TODO:ここで追加のフォームの保存もするため、requestを引数として受ける。argsで受け取っても良いが混乱するので。
    def save(self, request, commit=True, *args, **kwargs):

        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.filter(username=username)[0]
            fields_to_update = ("username","u_last_name","u_first_name","u_last_name_kana","u_first_name_kana","email","phone_number")
            [setattr(user, field, self.cleaned_data[field]) for field in fields_to_update]
            user.save()
        else:
            #ここで、ユーザーモデルのオブジェクト作成を行っている(ただし、保存をしない)
            user    = super().save(commit=False)

            #ここで生のパスワードをハッシュ化した上で、モデルオブジェクトの属性にセットする。
            password = self.cleaned_data["password1"]
            if password:
                user.set_password(password)

            if commit:
                user.save()

        #以降、質問者・回答者の追加情報を記録
        copied          = request.POST.copy()
        copied["user"]  = user.id
        
        question_form   = QuestionUserForm(copied)

        #バリデーションOKになるには、userとseriousnessがモデルで定義したルールに則っていればよい。それ以外に余計なものが入っていたとしてもNGにはならない(除外されるだけ)
        if question_form.is_valid():
            print("質問者ユーザー登録")
            question_form.save()
        else:
            print(question_form.errors)
            print("質問者ユーザーではない")

        answer_form     = AnswerUserForm(copied)

        if answer_form.is_valid():
            print("回答者ユーザー登録")
            answer_form.save()
        else:
            print(answer_form.errors)
            print("回答者ユーザーではない")
            
        #ここでuserをreturnしなければアカウント新規作成ページから、ログイン後のページへ遷移しない
        #ログイン後のページに遷移するため、userのis_activeをチェックした上で遷移する。もし、userオブジェクトが返却されなければNoneが入る。分岐でNoneに対してis_activeは存在し得ない。故にエラーが出る。
        return user



class UpdateForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']


from django.dispatch import receiver
from django.db.models.signals import pre_save
#from django.contrib.auth.models import User
