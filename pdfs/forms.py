from django import forms
from pdfs.models import Pdf_Upload


class PdfUploadForm(forms.ModelForm):
    book_content=forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    class Meta:
        fields=['book_title','book_author','book_subject','book_publisher','book_version','book_content']
        model=Pdf_Upload
        
class SubjectSelect(forms.ModelForm):
    class Meta:
        fields=['book_subject',]
        model=Pdf_Upload