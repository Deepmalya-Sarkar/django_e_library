from django.urls import path
from . import views
app_name='pdfs'
urlpatterns = [
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('student_dashboard/select/',views.select_book,name='select_book_std'),
    path('student_list/',views.StudentList.as_view(),name='student_list'),
    path('pdf/',views.render_pdf_view,name='generate'),
    # path('teacher_dashboard/upload/',views.UploadCreateView.as_view(),name='upload_book'),
    path('teacher_dashboard/upload/',views.PdfUpload,name='upload_book'),
    path('teacher_dashboard/select/',views.select_book,name='select_book'),
    path('teacher_dashboard/<str:username>/my_list/',views.My_List.as_view(),name='my_list'),
    path('teacher_dashboard/book_details/<int:pk>/',views.Book_Details.as_view(),name='book_details'),
    path('teacher_dashboard/book_update/<int:pk>/',views.BookUpdateView.as_view(),name='book_update'),
    path('teacher_dashboard/book_delete/<int:pk>/',views.BookDeleteView.as_view(),name='book_delete')
]