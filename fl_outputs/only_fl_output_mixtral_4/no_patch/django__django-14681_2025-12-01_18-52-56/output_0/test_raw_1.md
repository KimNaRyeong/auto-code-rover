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
from django.http import HttpRequest

# Minimal Django project settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'csrfbug.settings'

# Settings
MEDIA_ROOT = settings.MEDIA_ROOT = 'media/'
FILE_UPLOAD_MAX_MEMORY_SIZE = settings.FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 102