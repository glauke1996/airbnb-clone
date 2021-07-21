from django import forms
from django.forms.widgets import Textarea


class AddCommentForm(
    forms.Form
):  # we don't use the modelform cuz need to intercept save method
    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Add a Comment"})
    )
