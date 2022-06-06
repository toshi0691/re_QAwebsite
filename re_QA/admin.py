from django.contrib import admin
from .models import Topic,TopicReply, QuestionUser,AnswerUser,AnswerUserProfile

# Register your models here.


class AnswerUserAdmin(admin.ModelAdmin):
    list_display    = ["user","u_first_name","u_last_name","company","approval"]
    list_editable   = ["approval"]
    
    def u_first_name(self,obj):
        return obj.user.u_first_name

    def u_last_name(self,obj):
        return obj.user.u_last_name




admin.site.register(QuestionUser)
admin.site.register(AnswerUser,AnswerUserAdmin)
admin.site.register(AnswerUserProfile)
admin.site.register(Topic)
admin.site.register(TopicReply)
