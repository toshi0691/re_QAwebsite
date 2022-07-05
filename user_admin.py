# coding: utf8 

#実行方法
# python manage.py shell < user_admin.py
# BaseCommand を作ってしまう
#  https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

from turtle import end_fill
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
# 5分以内に登録が終わっていないユーザを見つけて消去する

import datetime
import pytz
tokyo = pytz.timezone('Asia/Tokyo')
now = datetime.datetime.now(tokyo)

registration_window_seconds = datetime.timedelta(seconds=60) 
emails_not_verified = EmailAddress.objects.filter(verified=False)

for email in emails_not_verified: 
    print(email.user)
    print('abs')
    if email.user.date_joined + registration_window_seconds < now:
        print('abc')
        email.user.delete()
        # print('ok') 
        # email.user.save()
        # print('yes')
        


# type(now)
# type(registration_window_seconds)
# type(email.user.date_joined)
# print(now)
# print(registration_window_seconds)
# print(email.user.date_joined)


#タイムゾーンなし時間(naive)を入れる
# a = '2022-06-26 22:00:00'
# #タイムゾーンなし時間をdatetimeオブジェクトに変換する
# a_unaware = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
# import pytz
# #Tokyoタイムゾーンを使えるようにする
# tokyo = pytz.timezone('Asia/Tokyo')
# #タイムゾーンなしdatetimeオブジェクトをtokyoタイムゾーンオブジェクトに変換する
# a_aware = tokyo.localize(a_unaware)

# #datetime.datetime(2022, 6, 26, 22, 0, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)

# c = datetime.datetime.now()
# print(c)
# c_loc = tokyo.localize(c)
# #datetime.datetime(2022, 6, 26, 6, 48, 20, 55432, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)
# print(c_loc)
# e = c_loc - a_aware
# print(e)
# d = datetime.datetime.now(tokyo)
# print(d)
# f = d - a_aware
# print(f)