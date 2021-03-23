from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from pdfs.validators import validate_is_pdf
# Create your models here.

class Pdf_Upload(models.Model):
    subjects=[
        ("C","C"),
        ("C++","C++"),
        ("Java","Java"),
        ("Python","Python"),
        ("Architechture","Architechture"),
        ("HTML","HTML"),
        ("CSS","CSS"),
        ("Javascript","Javascript"),
    ]
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    book_title=models.CharField(max_length=255)
    book_author=models.CharField(max_length=255)
    book_publisher=models.CharField(max_length=255)
    book_version=models.CharField(max_length=255)
    book_subject=models.CharField(max_length=50,choices=subjects,default='C')
    book_content=models.FileField(upload_to='books',validators=(validate_is_pdf,))

    def __str__(self):
        return "{}".format(self.book_title)
    
    def get_absolute_url(self):
        return reverse('pdfs:book_details', kwargs={'pk': self.pk})