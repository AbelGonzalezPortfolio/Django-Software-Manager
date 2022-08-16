from django import forms
from . import models


class ComputerSelect(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Computer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
