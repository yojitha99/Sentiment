from django import forms
from movieapp.models import Movie
from movieapp.models import Moviereview
class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields="__all__"
class MoviereviewForm(forms.ModelForm):
    class Meta:
        model=Moviereview
        fields=['review']
