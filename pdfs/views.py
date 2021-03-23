from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.models import User
from users.models import Profile
from pdfs.models import Pdf_Upload
from django.contrib import messages
from pdfs.forms import SubjectSelect,PdfUploadForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from ebook.decorators import unauthenticated_user,allowed_users
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
#For PDF creation
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa 
# Create your views here.

@login_required
@allowed_users(allowed_roles=['Teacher'])
def teacher_dashboard(request):
    return render(request,'pdfs/teacher_dashboard.html')

@login_required
@allowed_users(allowed_roles=['Student'])
def student_dashboard(request):
    return render(request,'pdfs/student_dashboard.html')



@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class StudentList(LoginRequiredMixin,ListView):
    model=User
    template_name='pdfs/student_list.html'
    context_object_name='students'

    def get_queryset(self):
        user=get_list_or_404(Profile,designation='STUDENT')
        return user

@login_required
@allowed_users(allowed_roles=['Teacher'])
def PdfUpload(request):
    if request.method == 'POST':
        form = PdfUploadForm(request.POST, request.FILES)
        form.instance.author=request.user
        if form.is_valid():
            form.save()
            messages.success(request,"Uploaded Successfully")
            return redirect('pdfs:teacher_dashboard')
    else:
        form = PdfUploadForm()
    return render(request, 'pdfs/pdf_upload_form.html', {'form': form})



# @method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
# class UploadCreateView(LoginRequiredMixin,CreateView):
#     fields=('book_title','book_author','book_subject','book_publisher','book_version','book_content')
#     model=Pdf_Upload

#     def form_valid(self,form):
#         form.instance.author=self.request.user
#         return super().form_valid(form)

@login_required
def select_book(request):
    if request.method=="POST":
        s_form=SubjectSelect(request.POST)
        if s_form.is_valid():
            book_subject=s_form.cleaned_data.get('book_subject')
            books=Pdf_Upload.objects.filter(book_subject=book_subject).order_by('book_title')
            # books=get_list_or_404(Pdf_Upload,book_subject=book_subject)
            return render(request,'pdfs/book_list.html',{'books':books})
    else:
        s_form=SubjectSelect()
    return render(request,'pdfs/book_select.html',{'s_form':s_form})

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class My_List(LoginRequiredMixin,ListView):
    model=Pdf_Upload
    template_name='pdfs/my_list.html'
    context_object_name='books'

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Pdf_Upload.objects.filter(author=user).order_by('book_title')

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class Book_Details(LoginRequiredMixin,DetailView):
    model=Pdf_Upload
    context_object_name='books'

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class BookUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    fields=('book_title','book_author','book_subject','book_publisher','book_version','book_content')
    model=Pdf_Upload

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        pdf_upload=self.get_object()
        if self.request.user ==pdf_upload.author:
            return True
        return False

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class BookDeleteView(LoginRequiredMixin,DeleteView):
    model=Pdf_Upload
    success_url=reverse_lazy('pdfs:teacher_dashboard')

    def test_func(self):
        pdf_upload=self.get_object()
        if self.request.user ==pdf_upload.author:
            return True
        return False


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_pdf_view(request):
    template_path = 'pdfs/pdf_list.html'
    students=Profile.objects.filter(designation='STUDENT')
    context = {'students':students}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_list.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



