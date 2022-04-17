from django.shortcuts import render,redirect
from django.views import View
from .models import Topic
from .forms import TopicForm

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

        return redirect("re_QA:index")

#urls.pyから呼び出せるようにするために.as_view()を使う
#クライアントがトップページにアクセスしたときは、GETされているので、Index.Viewのなかではget時はindex.htmlを連らリングするのでindex.html
index   = IndexView.as_view()

#関数ベースのビュー
'''
def index(request):
return render(request, "re_QA/index.html")
'''
