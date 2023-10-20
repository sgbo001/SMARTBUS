from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class SearchForm(forms.Form):
    from_post_code = forms.CharField(label='From', max_length=100, required=True)
    to_post_code = forms.CharField(label='To', max_length=100, required=True)
    date_time = forms.DateTimeField(label='Date Time', widget=forms.DateInput(attrs={'type': 'datetime-local'}))

    class Meta:
        widgets = {
            'date_time': forms.DateInput(attrs={'type': 'datetime-local'}),
        }


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['from_post_code'].widget.attrs.update({'placeholder': 'Enter Post Code'})
        self.fields['to_post_code'].widget.attrs.update({'placeholder': 'Enter Post Code'})
        self.fields['date_time'].widget.attrs.update({'placeholder': 'Enter Date/Time'})
