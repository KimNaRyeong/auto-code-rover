import os
import sys
from django.db import models
from django.core.exceptions import AssertionError

# Create a simple Django project and app
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
import django
django.setup()

class Category(models.Model):
    name = models.CharField(max_length=255)

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

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
    # Create some sample data
    category = Category.objects.create(name='Test Category')
    for i in range(10):
        Post.objects.create(category=category, title=f'Post {i}')

    # Try to prefetch a slice of related objects
    categories = Category.objects.prefetch_related(
        models.Prefetch('post_set',
                        queryset=Post.objects.all()[:3],
                        to_attr='example_posts')
    )

    # This should raise an AssertionError
    list(categories)

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
