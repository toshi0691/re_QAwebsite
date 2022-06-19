#実行方法
# python manage.py shell < user_admin.py
# BaseCommand を作ってしまう
#  https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

from re_QA.models import QuestionUser, AnswerUser
qu = QuestionUser.objects.all()
# qu[0]
# qu[0].__dict__
# {'_state': <django.db.models.base.ModelState object at 0x7fd9f18c9190>, 'id': 1, 'user_id': UUID('944db207-0ccf-4d46-8cc3-ebce0aa60576'), 'resident_area': 'q', 'resident_style': '1', 'email_notification': True, 'registration_time': datetime.datetime(2022, 6, 19, 12, 46, 35, 798495, tzinfo=datetime.timezone.utc)}
# >>> qu[0].user.email
#'yasuhiroono.samurai@gmail.com'
from allauth.account.models import EmailAddress
email_yo = EmailAddress.objects.all()[1]
# email_yo.__dict__
# {'_state': <django.db.models.base.ModelState object at 0x7fd9f18c9a60>, 'id': 17, 'user_id': UUID('944db207-0ccf-4d46-8cc3-ebce0aa60576'), 'email': 'yasuhiroono.samurai@gmail.com', 'verified': True, 'primary': True}

# 未登録のユーザを集める
# 制限時間内に登録が終わっていない人
# EmailAddressのみから判断できる
import datetime
now = datetime.datetime.now()
registration_window_seconds = datetime.timedelta(seconds=60*5) # 5分
emails_not_verified = EmailAddress.objects.filter(verified=False)
for email in emails_not_verified:
    # 5分以内に登録が終わっていないユーザを見つけて消去する
    if email.user.registration_time +  registration_window_seconds < now:
        # TODO
        email.user.delete()
        email.user.save()


