from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 부모의 생성자를 호출해줘야, Form 필드들이 생성이 됩니다.
        self.fields  # 이렇게 생성된 필드들은 self.fields를 통해 접근하실 수 있습니다.
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

