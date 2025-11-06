from django.db import models
from django.contrib import admin
from django.urls import path
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    class Post(models.Model):
        title = models.CharField(max_length=255)
        authors = models.ManyToManyField("User", related_name="posts")

    class User(models.Model):
        email = models.EmailField(unique=True)

    admin.site.register(Post, PostAdmin=admin.ModelAdmin(search_fields=("title", "authors__email")))

    post = Post(title="Test", authors=[User(email="test@example.com")])
    post.save()
    from django.contrib.admin.utils import lookup_field
    from django.contrib.admin.views.main import ChangeList

    class PostAdmin(admin.ModelAdmin):
        search_fields = ("title", "authors__email")

    admin.site.register(Post, PostAdmin)

    post_list = ChangeList(None, None)
    post_list.search = 'my'
    post_list.get_queryset = lambda: Post.objects.all()
    post_list.queryset = post_list.get_queryset()

    from django.contrib.admin.actions import delete_selected

    try:
        delete_selected(admin.site._registry[Post], post_list.queryset)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error occurred"
    else:
        print("No error occurred")
        exit(0)

except Exception as e:
    print_stacktrace(e)
    assert False, "Error occurred"

