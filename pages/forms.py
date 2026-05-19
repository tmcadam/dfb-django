from django import forms
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

from .models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'body']
        widgets = {
            'body': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2 font-weight-bold'
        self.helper.field_class = 'col-sm-10'
