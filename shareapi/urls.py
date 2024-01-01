# file_sharing/urls.py

from django.urls import path
from .views import upload_file, list_files, signup_view, login_view, email_verify

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('email-verify/<int:user_id>/', email_verify, name='email_verify'),
   # path('download-file/<int:file_id>/', download_file, name='download_file'),
    path('upload-file/', upload_file, name='upload_file'),
    path('list-files/', list_files, name='list_files'),
    
]

