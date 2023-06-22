from django.forms import ModelForm
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=150) #текст запроса
    catid = forms.IntegerField()


from .models import Comment
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate']