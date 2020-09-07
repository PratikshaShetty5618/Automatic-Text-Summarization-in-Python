from django import forms
from django.db.models import *
from .models import Summarized

class InputForm(forms.ModelForm):
    class Meta:
        model = Summarized
        fields = ("text_input",)

class ResultForm(forms.ModelForm):
	class Meta:
		model = Summarized
		fields = ("text_input","text_output")

class SaveForm(forms.ModelForm):
	class Meta:
		model = Summarized
		fields = ("text",)
			
		



