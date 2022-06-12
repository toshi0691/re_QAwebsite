from tabnanny import verbose
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid 
#from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator, RegexValidator
# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    id                 = models.UUIDField( default=uuid.uuid4, primary_key=True, editable=False )
    username           = models.CharField(
                            _('username'),
                            max_length=150,
                            unique=True,
                            help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                            validators=[username_validator],
                            error_messages={
                                'unique': _("A user with that username already exists."),
                            },
                        )
    u_last_name        = models.CharField(verbose_name='姓', max_length=20)
    u_first_name       = models.CharField(verbose_name='名', max_length=20)
    u_last_name_kana   = models.CharField(verbose_name='セイ', max_length=30)
    u_first_name_kana  = models.CharField(verbose_name='メイ', max_length=30)
    
    email              = models.EmailField(_('email address'))
    #phone_number       = PhoneNumberField(verbose_name='電話番号',unique = True, null = False)
    phone_number       = models.CharField(verbose_name='電話番号',
                                        validators=[RegexValidator(r'^0[0-9]{9,10}$', '正しい電話番号を入力して下さい')
                                                    ],max_length=11)
    source = models.CharField(verbose_name='紹介方法', max_length=30, blank=True)

######################################################

    is_staff           = models.BooleanField(
                            _('staff status'),
                            default=False,
                            help_text=_('Designates whether the user can log into this admin site.'),
                        )
    is_active          = models.BooleanField(
                        _('active'),
                        default=True,
                        help_text=_(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                        ),
                        )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects     = UserManager()

    EMAIL_FIELD     = 'email'
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email','u_first_name','u_last_name','u_first_name_kana','u_last_name_kana','phone_number']
    #管理画面の表示で、ある類いのユーザをまとめて設定を変更したいときには複数のユーザリンクをクリックして編集できるようにでき、
    #単体を編集したいときは、単体ユーザの方が使われるようにするという設定
    class Meta:
        verbose_name        = _('user')
        verbose_name_plural = _('users')
        #abstract            = True         #←ここをコメントアウトしないとカスタムユーザーモデルは反映されず、マイグレーションエラーを起こす。
        permissions = (("is_activated", "User is activated"),)
        
    def clean(self):
        super().clean()
        self.email  = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        full_name = "%s %s" % (self.u_first_name, self.u_last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.u_first_name
    
##################################################################

'''
class AnswerUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id                 = models.UUIDField( default=uuid.uuid4, primary_key=True, editable=False )
    
    resident_area      = models.CharField(verbose_name='居住エリア', max_length=30)
    resident_style     = models.CharField(verbose_name='居住形態', max_length=30)
'''