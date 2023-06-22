from django.forms import ModelForm
from django import forms
from .models import ContactMessage

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject','message']
        widgets = {
            'name'   : forms.TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
            'subject' : forms.TextInput(attrs={'class': 'input','placeholder':'Subject'}),
            'email'   : forms.EmailInput(),
            'message' : forms.Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=150) #текст запроса
    catid = forms.IntegerField()