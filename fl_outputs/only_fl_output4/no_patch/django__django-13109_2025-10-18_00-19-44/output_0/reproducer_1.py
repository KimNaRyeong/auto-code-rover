import os
import django
from django.conf import settings
from django.db import models, connection
from django.core.management import call_command

# Define the standalone Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    SECRET_KEY='reproducer',
)

django.setup()

# Models definition
class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)

class Article(models.Model):
    title = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    objects = ArticleManager()

class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

# Create tables directly in the database
with connection.schema_editor() as editor:
    editor.create_model(Article)
    editor.create_model(FavoriteArticle)

# Django forms to simulate user action
from django import forms

class FavoriteArticleForm(forms.ModelForm):
    class Meta:
        model = FavoriteArticle
        fields = '__all__'

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    archived_article = Article.objects.create(title="Archived Article", archived=True)
    form_data = {'article': archived_article.pk}
    form = FavoriteArticleForm(data=form_data)
    if form.is_valid():
        # Expected to not validate, but if it does, the issue is not present
        print("The issue has been fixed.")
        sys.exit(0)
    else:
        raise AssertionError("Form did not validate for a valid archived article id.")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
