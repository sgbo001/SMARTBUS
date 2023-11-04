from django import forms
from .models import Review
from bus.models import Bus

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['arrival_time', 'full_name','rating', 'comment']
    


