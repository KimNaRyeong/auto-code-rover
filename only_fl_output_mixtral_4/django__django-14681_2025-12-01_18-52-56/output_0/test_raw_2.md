 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import shutil
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.test import RequestFactory, TestCase
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse

# Minimal Django project settings for reproducing the issue
settings.configure(
    DEBUG=True,
    SECRET_KEY='not-so-secret',
    ROOT_URLCONF='reproducer',
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'reproducerapp',
    ],
    MEDIA_URL='/media/',
    MEDIA_ROOT='media/',
    FILE_UPLOAD_MAX_MEMORY_SIZE=1024 * 1024,
    FILE_UPLOAD_TEMP_DIR=os.path.join('media', 'tmp'),
)

os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
os.makedirs(settings.FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# Minimal Django app for reproducing the issue
urlpatterns = [
    path('admin/', include(admin.site.urls)),
    path('admin/app/file/add/', csrf_exempt(FileCreateView.as_view())),
]

class FileCreateView:
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('File uploaded.')
        return HttpResponse('Invalid request.')

def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Test case for reproducing the issue
class TestFileUpload(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.request = self.factory.post('/admin/app/file/add/', {
            'file': open('reproducer.py', 'rb'),
        })
        self.request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        setattr(self.request, '_dont_enforce_csrf_checks', True)

    def test_file_upload(self):
        # Scenario 1: File uploads work as expected
        shutil.rmtree(settings.FILE_UPLOAD_TEMP_DIR, ignore_errors=True)
        os.makedirs(settings.FILE_UPLOAD_TEMP_DIR, exist_ok=True)
        response = FileCreateView.dispatch(self.request, None)
        self.assertEqual(response.status_code, 200)

        # Scenario 2: File uploads work only for files that fit in FILE_UPLOAD_MAX_MEMORY_SIZE
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        os.makedirs(settings.MEDIA_ROOT, exist_