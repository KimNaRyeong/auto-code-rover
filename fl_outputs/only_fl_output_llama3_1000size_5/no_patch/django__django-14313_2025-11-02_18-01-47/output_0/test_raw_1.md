Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment
from django.core.management import execute_from_command_line
from django.conf import settings

# Set up Django environment for testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
setup_test_environment()

# Create the project structure
project_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs('reproducer', exist_ok=True)
os.chdir(project_dir)

# Create the models
models_file_path = 'reproducer/models.py'
with open(models_file_path, 'w') as f:
    f.write("""
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("User", related_name="posts")

class User(models.Model):
    email = models.EmailField(unique=True)
""")

# Create the admin
admin_file_path = 'reproducer/admin.py'
with open(admin_file_path, 'w') as f:
    f.write("""
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")
""")

# Create the urls
urls_file_path = 'reproducer/urls.py'
with open(urls_file_path, 'w') as f:
    f.write("""
from django.urls import path
from .admin import admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
]
""")

try:
    # Run the Django app
    execute_from_command_line(['manage.py', 'runserver'])
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script creates a new Django project, defines the models and admin configuration, and then runs the Django development server. If an `AssertionError` is raised during this process, it prints the stack trace using the provided function and exits with code 1.