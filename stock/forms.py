from django import forms

class GetDataForm(forms.Form):
    year_start = forms.CharField(label='Год', max_length=4)
    year_end = forms.CharField(label='Год', max_length=4)
    month_start = forms.CharField(label='Месяц', max_length=2)
    month_end = forms.CharField(label='Месяц', max_length=2)
    day_start = forms.CharField(label='День', max_length=2)
    day_end = forms.CharField(label='День', max_length=2)

class PredicationForm(forms.Form):
    companyName = forms.CharField(label='Компания', max_length=50)
    year = forms.CharField(label='Год', max_length=4)
    month = forms.CharField(label='Месяц', max_length=2)
    day = forms.CharField(label='День', max_length=2)