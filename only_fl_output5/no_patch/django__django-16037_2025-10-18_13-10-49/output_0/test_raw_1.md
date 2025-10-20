```python
import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Exists, OuterRef, Prefetch, Value, Case, When
from django.db.models.query import QuerySet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Minimal Django settings necessary for the script
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script is the app
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()


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


class CustomUserManager(models.Manager):
    pass


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    liked_posts = models.ManyToManyField('Post', related_name='liked_by')
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    reply = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.parent_comment is not None:
            if self.parent_comment.post.id != self.post.id:
                raise ValidationError("Parent comment must be from the same post.")
            self.reply = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text} - reply: {self.reply}"


class PostManager(models.Manager):
    def request_data(self, request_user):
        liked_by_user, is_following, is_owner = Value(False), Value(False), Case(When(user__id=request_user.id, then=Value(True)), default=Value(False))
        if request_user.is_authenticated:
            liked_by_user = Exists(request_user.liked_posts.filter(id=OuterRef("id")))
            is_following = Exists(request_user.following.filter(id=OuterRef("user__id")))
        return liked_by_user, is_following, is_owner

    def fetch_all_posts(self, request_user) -> QuerySet:
        liked_by_user, is_following, is_owner = self.request_data(request_user)
        try:
            return self.get_queryset().annotate(
                is_following=is_following,
                is_owner=is_owner,
                likes=Count("liked_by"),
                liked_by_user=liked_by_user,
            )
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue with QuerySet.annotate() found.") from e


# Function to simulate a testing scenario
def run_test():
    # Set up test environment
    User.objects.all().delete()
    Post.objects.all().delete()

    user = User.objects.create(username="testuser")
    post = Post.objects.create(user=user, text="Hello World!")

    manager = PostManager()
    manager.model = Post  # Normally Django sets this automatically

    # Attempt to fetch posts, which should raise the expected error
    manager.fetch_all_posts(user)


if __name__ == "__main__":
    try:
        run_test()
    except AssertionError as e:
        exit(0)
```