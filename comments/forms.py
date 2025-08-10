from django import forms
from comments.models import Comment

class SubmitCommentForm(forms.ModelForm):
    
    url = forms.CharField(initial="", required=False)

    class Meta:
        model = Comment
        fields = ["name", "email", "comment", "biography", "url"]
        widgets = {'biography': forms.HiddenInput()}
