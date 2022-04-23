from django.shortcuts import render,redirect
from django.views import View
from .models import Topic
from .forms import TopicForm
from .models import PhotoList,DocumentList,TopicReply
from .forms import PhotoListForm,DocumentListForm,TopicReplyForm
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
        
        form    = TopicForm(request.POST)

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



class QuestionsView(View):
    
    def get(self, request, *args, **kwargs):
        
        topics  = Topic.objects.all()
        context = { "topics":topics }
        
        return render(request,"re_QA/questions.html",context)

questions    = QuestionsView.as_view()

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
   
class SingleView(View):
    def get(self, request, pk, *args, **kwargs):
        
        context = {}
        context["topic"]   = Topic.objects.filter(id=pk).first()
        context["replies"]  = TopicReply.objects.filter(topic=pk)
        
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