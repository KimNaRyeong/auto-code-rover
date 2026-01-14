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

# Models
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    posts = models.related.RelatedManager()
    liked_posts = models.related.RelatedManager()
    comments = models.related.RelatedManager()
    about = models.CharField(blank=True, max_length=255)
    photo = models.FileField(
        blank=True,
        null=True,
        upload_to="",
        validators=[],
    )
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )
    objects = models.Manager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username}"

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
    objects = models.Manager()

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f"{self.text}"

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

    class Meta:
        db_table = "comments"

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.parent_comment is not None:
            if self.parent_comment.post.id != self.post.id:
                raise ValueError("Parent comment must be from the same post.")
            self.reply = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text} - reply: {self.reply}"

# Managers
class PostManager(models.Manager):
    def request_data(self, request_user):
        liked_by_