```python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

# Configure Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'reproducer_app'
    ]
)

# Creating a new application to contain the models and admin configuration for reproduction
app_name = 'reproducer_app'
os.makedirs(app_name, exist_ok=True)
with open(os.path.join(app_name, '__init__.py'), 'w'):
    pass

# Create models.py
with open(os.path.join(app_name, 'models.py'), 'w') as f:
    f.write("""
from django.db import models

class Reporter(models.Model):
    name = models.CharField(max_length=50)

class Journalist(Reporter):
    class Meta:
        proxy = True

class SpecialJournalist(Journalist):
    class Meta:
        proxy = True

class Article(models.Model):
    journalist = models.ForeignKey(Journalist, on_delete=models.CASCADE)
""")

# Create admin.py to register models and their admin representation
with open(os.path.join(app_name, 'admin.py'), 'w') as f:
    f.write("""
from django.contrib import admin
from .models import SpecialJournalist, Article

class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'journalist'

@admin.register(SpecialJournalist)
class SpecialJournalistAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
""")

# Make migrations and migrate to prevent system check errors unrelated to the issue
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
execute_from_command_line(['django-admin', 'makemigrations', app_name])
execute_from_command_line(['django-admin', 'migrate'])

# Test reproducer
def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from django.contrib import admin
    from reproducer_app.models import SpecialJournalist
    admin.site.check()

    assert False, "The system check passed when an error was expected."

except AssertionError as ae:
    raise ae

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```