from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from re_QA.forms import QuestionUserForm,AnswerUserForm
from re_QA.models import QuestionUser,AnswerUser, ValidationCode
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ("username","u_last_name","u_first_name","u_last_name_kana","u_first_name_kana","email","phone_number","source")
        #

    def clean_source(self):
        # 質問者の場合は登録コードのバリデーションはしない
        if 'company' not in self.cleaned_data:
            return self.cleaned_data['source']

        code = self.cleaned_data['source']
        code_source_map ={x.code:x.source for x in ValidationCode.objects.all()}
        if code not in code_source_map.keys():
            raise ValidationError("登録コードが間違っています")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return code_source_map[code]

    #TODO:ここで追加のフォームの保存もするため、requestを引数として受ける。argsで受け取っても良いが混乱するので。
    def save(self, request, commit=True, *args, **kwargs):

        #ここで、ユーザーモデルのオブジェクト作成を行っている(ただし、保存をしない)
        #user    = super().save(commit=False)
        #バリデーションを通過したusernameのみusername変数に入れている？
        username =self.cleaned_data['username']

        #ここで生のパスワードをハッシュ化した上で、モデルオブジェクトの属性にセットする。
        if CustomUser.objects.filter(username=username).exists():
            #ユーザ登録情報更新の場合
            user = CustomUser.objects.filter(username=username)[0]
            fields_to_update = ("username","u_last_name","u_first_name","u_last_name_kana","u_first_name_kana","email","phone_number")
            [setattr(user, field, self.cleaned_data[field]) for field in fields_to_update]
            user.save()
        else:
            #ユーザ新規作成の場合
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
        qa_user_identified = False
        #バリデーションOKになるには、userとseriousnessがモデルで定義したルールに則っていればよい。それ以外に余計なものが入っていたとしてもNGにはならない(除外されるだけ)
        if question_form.is_valid():
            print("質問者ユーザー登録")
            question_form.save()
        else:
            print("質問者ユーザーではないか、既に質問者ユーザが存在する")
            print(question_form.errors)
            if QuestionUser.objects.filter(user=user.id):
                quser = QuestionUser.objects.filter(user=user.id)[0]
                fields_to_update = ("resident_area", "resident_style")
                [setattr(quser, field, copied[field]) for field in fields_to_update]
                quser.save()
                qa_user_identified = True



        answer_form     = AnswerUserForm(copied)

        if answer_form.is_valid():
            print("回答者ユーザー登録")
            #user.is_active = False
           
            answer_form.save()
        else:
            print("回答者ユーザーではないか、すでに回答者ユーザが存在する")
            if not qa_user_identified and AnswerUser.objects.filter(user=user.id):
                quser = AnswerUser.objects.filter(user=user.id)[0]
                fields_to_update = ("company",)
                [setattr(quser, field, copied[field]) for field in fields_to_update]
                quser.save()
            
        #ここでuserをreturnしなければアカウント新規作成ページから、ログイン後のページへ遷移しない
        #ログイン後のページに遷移するため、userのis_activeをチェックした上で遷移する。もし、userオブジェクトが返却されなければNoneが入る。分岐でNoneに対してis_activeは存在し得ない。故にエラーが出る。
        return user

class UpdateForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']



    