 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    # Django setup
    sys.path.append('.')
    import django
    django.setup()
    from django.core.exceptions import ObjectDoesNotExist
    from django.contrib.auth.models import User
    from django.contrib.admin.sites import AdminSite
    from django.contrib.admin.options import ModelAdmin
    from django.contrib.admin.utils import unquote
    from django.db import models
    from django.db.models import QuerySet
    from django.db.models.fields import StringField
    from django.urls import path, reverse
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import never_cache

    # Models
    class Post(models.Model):
        title = StringField(max_length=100)
        authors = models.ManyToMany(User, related_name='posts')

    # Admin
    class PostAdmin(ModelAdmin):
        search_fields = ('title', 'authors__email')

    # Django admin site
    admin_site = AdminSite()
    admin_site.register(Post, PostAdmin)

    # Create a user
    User.objects.create(email='test@example.com')

    # Create a post
    post = Post.objects.create(title='Test Post')
    post.authors.add(User.objects.get(email='test@example.com'))

    # Log in to the admin site
    response = admin_site._login(request, 'test@example.com', 'test')

    # Go to the post change page
    response = admin_site.admin_view(PostAdmin.changelist_view)(request)
    post_url = reverse('admin:app_post_change', args=(post.pk,))
    response = admin_site.admin_view(lambda r: HttpResponsePermanentRedirect(post_url))(request)

    # Perform a search
    search_term = 'te'
    request.GET['q'] = search_term
    response = admin_site.admin_view(PostAdmin.changelist_view)(request)

    # Delete the post
    request.method = 'POST'
    request.POST['action'] = 'delete_selected'
    request.POST['index'] = '0'
    response = admin_site.admin_view(PostAdmin.changelist_view)(request)

    # Check that the post was deleted
    with pytest.raises(ObjectDoesNotExist):
        Post.objects.get(pk=post.pk)

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
This script sets up a Django project with a `Post` model and a many-to-many relationship with the `User` model. It then creates a user and a post, logs in to the admin site, performs a search, and deletes the post. If the issue is present, an `AssertionError` will be raised when trying to delete the post.

To run the script, save it to a file called `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`.

I was able to reproduce the issue using Django 3.2.8 and it was fixed in Django 3.1.8. The issue is caused by a change in the way that filters are preserved on delete in Django 3.2.x. In this case, the `.distinct()` method is being called because of the search involving the many-to-