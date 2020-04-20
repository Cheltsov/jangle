from django import forms

class RegistrationForm(forms.Form):
    email = forms.CharField(label='E-mail', max_length=50)
    password = forms.CharField(label='Пароль', max_length=50)
    confirmationPassword = forms.CharField(label='Подтверждение пароля', max_length=50)