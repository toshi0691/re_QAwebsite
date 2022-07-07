from django.shortcuts import render,redirect, get_object_or_404
from django.views import View,generic
from .models import Topic,AnswerUser,QuestionUser,AnswerUserProfile
from .forms import AnswerUserForm, TopicForm, AnswerUserProfileForm
from users.forms import SignupForm, UpdateForm
from users.models import CustomUser
from .models import PhotoList,DocumentList,TopicReply
from .forms import PhotoListForm,DocumentListForm,TopicReplyForm #,RegisterUserForm
from allauth.account.models import EmailAddress
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import magic




ALLOWED_MIME    = [ "application/pdf" ]

class IndexView(View):

    def get(self, request, *args, **kwargs):

        try:
            email = request.user.email
            if EmailAddress.objects.filter(email=email, verified=True).exists() is False:
                return redirect('accounts/confirm-email/')

            # if not request.user.has_perm('users.is_activated'):
            #     return redirect('not_activated/')

        except AttributeError as _:
            #AnonymousUserは除外
            pass
        # if request.user.company
        
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
    
    # def get_queryset(self):
    #     queryset = Topic.objects.order_by('-create_at')
    #     keyword = self.request.GET.get('keyword')
    #     if keyword :
    #         queryset = queryset.filter(Q(genre__icontains = keyword)|(Q(comment__icontains = keyword)))
    #         context = { "searched_topics": queryset }
    #     return render("re_QA/searched_questions.html",context)
    #     # return super().get_queryset()
        
    def post(self, request, pk, *args, **kwargs):
            
        #if 'sort_own' in request.POST:
            #自分の質問のみを集めてリダイレクトするメソッド
            
            
        return redirect("re_QA:single",pk)
      
questions    = QuestionsView.as_view()

class SearchedQuestionsView(generic.ListView):
    model = Topic
    def get_queryset(self):
            
            keyword = self.request.GET.get('keyword')
            if not keyword :
                queryset = Topic.objects.none()
                return queryset
            queryset = Topic.objects.order_by('-dt')
            queryset = queryset.filter(Q(genre__icontains = keyword)|(Q(comment__icontains = keyword)))
            # context = { "searched_topics": queryset }
            return queryset
            
    
searched_questions    = SearchedQuestionsView.as_view()



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



#########################################回答者一覧ページ######################
class AnswerersView(View):
    
    def get(self, request, *args, **kwargs):
        
        profiles  = AnswerUserProfile.objects.all()
        context = { "profiles":profiles }
        
        return render(request,"re_QA/answerers.html",context)
        
    def post(self, request, pk, *args, **kwargs):
            
        #if 'sort_own' in request.POST:
            #自分の質問のみを集めてリダイレクトするメソッド
            
            
        return redirect("re_QA:each_answerer_profile",pk)
      
answerers    = AnswerersView.as_view()
#########################################個々の回答者プロフィールページ########################################
class EachAnswererProfileView(View):
    
    def get(self, request, pk, *args, **kwargs):
        
        #contextを辞書型にする
        context = {}
#Topicクラスのidがpkと一致する最初のオブジェクトに、"topic"というキーを割り当てる
###filterの中user=pkで合っている？id=pkだとエラーになるからそうしたが。##############
        context["answerer"]   = AnswerUserProfile.objects.filter(user=pk).first()
        
        if not context["answerer"]:
            print("存在しないのでリダイレクト") 
            return redirect("re_QA:index")
        
    # def profile(request, id):
        top = AnswerUserProfile.objects.all().order_by("-points")[:min(AnswerUserProfile.objects.count(),5)]
        if request.user.is_authenticated:
            profile = get_object_or_404(AnswerUserProfile,user=pk)
            if profile.points < 100:
                color = "#3498db"
                rank = "Amateur"
            elif profile.points < 1000:
                color = "#1abc9c"
                rank = "Trainee"
            elif profile.points < 2000:
                color = "gold"
                rank = "Professor"
            else:
                color = "red"
                rank = "Legend"
        else:
            profile = get_object_or_404(AnswerUserProfile,id=1)
            val = ""
            percent = 100

        queryset_list=Topic.objects.all().filter(user=profile).order_by("-dt")
        paginator = Paginator(queryset_list, 10)
        page = request.GET.get('page')
        username='Login'
        if request.user.is_active:
            username = request.user.username
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)


        queryset_list1=TopicReply.objects.all().filter(user=profile).order_by("-dt")
        paginator1 = Paginator(queryset_list1, 10)
        page1 = request.GET.get('page1')
        username='Login'
        if request.user.is_active:
            username = request.user.username
        try:
            queryset1 = paginator1.page(page1)
        except PageNotAnInteger:
            queryset1 = paginator1.page(1)
        except EmptyPage:
            queryset1 = paginator1.page(paginator1.num_pages)


        context={
            "profile":profile,
            "color":color,
            "rank": rank,
            "object_list":queryset,
            "page":"page",
            "object_list1":queryset1,
            "page1":"page1","q":Topic.objects.count(),"a":TopicReply.objects.count(),"u":AnswerUserProfile.objects.count(),"top":top
        }
        # return render(request,"profile.html",context)
        
        return render(request,"re_QA/each_answerer_profile.html",context)
        
      
each_answerer_profile    = EachAnswererProfileView.as_view()

#########################################ユーザ会員登録ページ#################################################

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
        form    = UpdateForm(request.POST, instance=user)
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



class CreateProfileView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated :
            print("未認証")
            return redirect("account_login")
        
        context = {}

        context["users"]         = AnswerUserProfile.objects.all()
        
        return render(request,"re_QA/create_profile.html",context)
    
    def post(self, request, *args, **kwargs):
    
    
        copied          = request.POST.copy()
        copied["user"]  = request.user.id
        form    = AnswerUserProfileForm(copied)
        
        
        if form.is_valid():
            print("バリデーションOK")
            
            #保存する
            form.save()
        else:
            print("バリデーションNG")

            #バリデーションNGの理由を表示させる
            print(form.errors)

        return redirect("re_QA:create_profile")
    
#urls.pyから呼び出せるようにするために.as_view()を使う
#クライアントがトップページにアクセスしたときは、GETされているので、Index.Viewのなかではget時はindex.htmlをレンダリングするのでindex.html
create_profile   = CreateProfileView.as_view()



class UpdateProfileView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print("未認証")
            return redirect("account_login")

        context = {}

        context["users"]         = CustomUser.objects.all()
        context["answer_user"]   = AnswerUser.objects.filter(user=request.user.id).first()
        context["question_user"] = QuestionUser.objects.filter(user=request.user.id).first()

        print(context["question_user"])


        return render(request,"re_QA/update_profile.html",context)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print("未認証")
            return redirect("account_login")

        user    = CustomUser.objects.filter(id=request.user.id).first()
        form    = AnswerUserProfileForm(request.POST, instance=user)
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

        return redirect("re_QA:update_profile")
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

def mail_confirm(request):
    if not EmailAddress.objects.filter(user=request.user.id, verified=True):
        return redirect("account_email_verification_sent") 

