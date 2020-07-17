from django import forms
from pdfs.models import Pdf_Upload

class SubjectSelect(forms.ModelForm):
    class Meta:
        fields=['book_subject',]
        model=Pdf_Upload