from django import forms
from crispy_forms.helper import FormHelper
from .models import Comment


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["biography", "name", "email", "comment", "approved"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2 font-weight-bold"
        self.helper.field_class = "col-sm-10"
