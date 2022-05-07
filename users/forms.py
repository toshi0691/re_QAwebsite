from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ("username","u_first_name","u_last_name","u_first_name_kana","u_last_name_kana","resident_area","resident_style","email","phone_number")
        #
        


    