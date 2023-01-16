from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import StatusModel, WorkersModel

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Имя пользователя уже занято")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароль не подходит")

        return password2

    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1', 'password2']
        labels = {
            
            'first_name':'Имя',
            'last_name':'Фамилия',
            'username':'Имя пользователя',
            'password1':'Пароль',
            'password2':'Подтверждение пароля'
        } 

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class StatusForm(forms.ModelForm):

    class Meta:
        model = StatusModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class WorkerForm(forms.ModelForm):
    class Meta:
        model = WorkersModel
        fields = '__all__'
        exclude = ('present', 'absent', 'total', 'total_hours', 'slug','vacation')
    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'