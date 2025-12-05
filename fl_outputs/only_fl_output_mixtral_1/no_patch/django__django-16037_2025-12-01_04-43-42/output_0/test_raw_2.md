 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import django
import sys
from django.db import models
from django.db.models import Count, Exists, Value, Case, When

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    posts = models.related.RelatedManager()
    liked_posts = models.related.RelatedManager()
    comments = models.related.RelatedManager()
    about = models.CharField(blank=True, max_length=255)
    photo = models.FileField(blank=True, null=True)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )
    objects = models.Manager()

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    comments = models.related.RelatedManager()
    user_id = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    text = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, related_name="liked_posts", blank=True
    )
    objects = PostManager()

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    replies = models.related.RelatedManager()
    post_id = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user_id = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    reply = models.BooleanField(default=False)
    parent_comment_id = models.IntegerField(null=True, blank=True)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

def print_query(query):
    print("SQL:")
    print(query.query)
    print("Params:")
    print(query.params)

def main():
    settings = django.conf.settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[__name__],
    )
    django.setup()

    # Create models
    User.objects.create(id=1, username="user1")
    User.objects.create(id=2, username="user2")
    Post.objects.create(id=1, user_id=1, text="Post 1")
    Post.objects.create(id=2, user_id=1, text="Post 2")
    Comment.objects.create(id=1, post_id=1, user_id=1, text="Comment 1