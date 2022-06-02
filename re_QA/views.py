from django.shortcuts import render,redirect
from django.views import View
from .models import Topic,AnswerUser,QuestionUser
from .forms import AnswerUserForm, TopicForm
from users.forms import SignupForm, UpdateForm
from users.models import CustomUser
from .models import PhotoList,DocumentList,TopicReply
from .forms import PhotoListForm,DocumentListForm,TopicReplyForm #,RegisterUserForm
from allauth.account.models import EmailAddress
from django.contrib.auth.mixins import LoginRequiredMixin
import magic



ALLOWED_MIME    = [ "application/pdf" ]

class IndexView(View):

    def get(self, request, *args, **kwargs):

        topics  = Topic.objects.all()
        context = { "topics":topics }
        
        return render(request,"re_QA/index.html",context)
    
    def post(self, request, *args, **kwargs):
        """
        posted  = Topic( comment = request.POST["comment"] )
        posted.save()
        """
        print(request.POST)
        copied          = request.POST.copy()
        copied["user"]  = request.user.id
        form    = TopicForm(copied)
        
        
        if form.is_valid():
            print("バリデーションOK")
            
            #保存する
            form.save()
        else:
            print("バリデーションNG")

            #バリデーションNGの理由を表示させる
            print(form.errors)

        return redirect("re_QA:questions")
    
#urls.pyから呼び出せるようにするために.as_view()を使う
#クライアントがトップページにアクセスしたときは、GETされているので、Index.Viewのなかではget時はindex.htmlをレンダリングするのでindex.html
index   = IndexView.as_view()

#################################質問を一覧表示するビュー#################################

class QuestionsView(View):
    
    def get(self, request, *args, **kwargs):
        
        topics  = Topic.objects.all()
        context = { "topics":topics }
        
        return render(request,"re_QA/questions.html",context)
        
    def post(self, request, pk, *args, **kwargs):
            
        #if 'sort_own' in request.POST:
            #自分の質問のみを集めてリダイレクトするメソッド
            
            
        return redirect("re_QA:single",pk)
      
questions    = QuestionsView.as_view()


###################################個別ページを表示するビュー###################################
   
class SingleView(View):
    def get(self, request, pk, *args, **kwargs):
    
#contextを辞書型にする
        context = {}
#Topicクラスのidがpkと一致する最初のオブジェクトに、"topic"というキーを割り当てる
        context["topic"]   = Topic.objects.filter(id=pk).first()
#TopicReplyクラスのtopicがpkと一致しているオブジェクトに、"replies"というキーを割り当てる
        context["replies"]  = TopicReply.objects.filter(topic=pk)
        
        if not context["topic"]:
            print("存在しないのでリダイレクト") 
            return redirect("re_QA:index")
        
        return render(request,"re_QA/single.html",context)
    
    def post(self, request, pk, *args, **kwargs):

        print(request.POST)

        #リクエストオブジェクトはイミュータブル(書き換え不可能)なデータなので下記はエラーになってしまう。
        #request.POST["topic"]   = pk

        #リクエストボディに対して何かを追加したい時、.copy()メソッドを使ってリクエストオブジェクトをコピーする
        copied          = request.POST.copy()
        copied["topic"] = pk


        form    = TopicReplyForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("re_QA:single",pk)
    
single   = SingleView.as_view()


#########################################自分のした質問を一覧表示させるメソッド######################

#########################################ユーザ会員登録ページ######################################

#########################################質問ユーザ会員登録情報編集ページ######################################

class UpdateQuestionUserView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print("未認証")
            return redirect("account_login")
        
        context = {}

        context["users"]         = CustomUser.objects.all()
        context["answer_user"]   = AnswerUser.objects.filter(user=request.user.id).first()
        context["question_user"] = QuestionUser.objects.filter(user=request.user.id).first()

        print(context["question_user"])



        return render(request,"re_QA/update_question_user.html",context)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print("未認証")
            return redirect("account_login")



        user    = CustomUser.objects.filter(id=request.user.id).first()
        form    = UpdateForm(request.POST,instance=user)
        # user_inf_a  = AnswerUser.objects.filter(user=request.user.id).first()
        # form_a  = AnswerUserForm(request.POST,instance=user_inf_a)
        # user_inf_b  = QuestionUser.objects.filter(user=request.user.id).first()
        # form_b  = QuestionUserForm(request.POST,instance=user_inf_b)

        if form.is_valid():
            print("バリデーションOK")
            form.save(request)
        else:
            print("バリデーションNG")
            print(form.errors)
            #form.save(request) 
        # if form_a.is_valid():
        #     print("バリデーションOK")
        #     form_a.save()
        # else:
        #     print("バリデーションNG")
        #     print(form_a.errors)
            
        # if form_b.is_valid():
        #     print("バリデーションOK")
        #     form_b.save()
        # else:
        #     print("バリデーションNG")
        #     print(form_b.errors)

        return redirect("re_QA:update_question_user")

update_question_user   = UpdateQuestionUserView.as_view()


#関数ベースのビュー
'''
def index(request):
return render(request, "re_QA/index.html")
'''

'''
class QuestionsView(View):
    
    def get(self, request, *args, **kwargs):

        topics  = Topic.objects.all()
        context = { "topics":topics }
        
        return render(request,"re_QA/index.html",context)

    def post(self, request, *args, **kwargs):
'''      

# class ProfileView(View, LoginRequiredMixin):
    
#     def get(self, request, *args, **kwargs):
        



class PhotoView(View):

    def get(self, request, *args, **kwargs):

        data    = PhotoList.objects.all()
        context = { "data":data }

        return render(request,"re_QA/photo.html",context)

    def post(self, request, *args, **kwargs):

        form    = PhotoListForm(request.POST, request.FILES)

        if form.is_valid():
            print("バリデーションOK")
            form.save()

        return redirect("re_QA:photo")

photo       = PhotoView.as_view()

class DocumentView(View):

    def get(self, request, *args, **kwargs):

        data    = DocumentList.objects.all()
        context = { "data":data }

        return render(request,"re_QA/document.html",context)

    def post(self, request, *args, **kwargs):

        form        = DocumentListForm(request.POST,request.FILES)
        mime_type   = magic.from_buffer(request.FILES["document"].read(1024) , mime=True)

        if form.is_valid():
            print("バリデーションOK")

            if mime_type in ALLOWED_MIME:
                form.save()
            else:
                print("このファイルは許可されていません。")

        return redirect("re_QA:document")

document    = DocumentView.as_view()

#############################メール認証のURLをクリックした後に会員登録が完了する###########################

def mail_confirm(self, request):
    if not EmailAddress.objects.filter(user=request.user.id, verified=True):
        return redirect("account_email_verification_sent") 


