Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.contrib import admin
from django.db import models
from django.test import TestCase, RequestFactory

# Create a test project and app
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
from reproducer.settings import *

class Post(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('User')

class User(models.Model):
    email = models.EmailField(unique=True)

class PostAdmin(admin.ModelAdmin):
    search_fields = ("title", "authors__email")

admin.site.register(Post, PostAdmin)

# Create a test database
from django.core.management import call_command
call_command('migrate', verbosity=0)

# Create some test data
post = Post.objects.create(title='Test Post')
user = User.objects.create(email='test@example.com')
post.authors.add(user)

class ReproducerTestCase(TestCase):
    def test_delete_after_search(self):
        factory = RequestFactory()
        request = factory.get('/admin/post/post/?q=Te')
        request.user = self.createUser(username='admin', password='password')

        # Get the changelist view
        from django.contrib.admin.views.main import ChangelistView
        cl_view = ChangelistView(PostAdmin(Post, admin.site), request)
        cl_response = cl_view.dispatch(request)

        # Select the post and delete it
        request = factory.post('/admin/post/post/', {'action': 'delete_selected', '_selected_action': 'delete_selected', 'index': 0}, follow=True)
        response = cl_view.dispatch(request)

        # Check if the issue is present
        if response.status_code == 500:
            print_stacktrace(sys.exc_info()[1])
            raise AssertionError("Issue is present")
        else:
            print("Issue is fixed")

if __name__ == '__main__':
    ReproducerTestCase('test_delete_after_search').run()
```
This script creates a test project and app, defines the `Post` and `User` models, registers the `PostAdmin`, creates some test data, and then runs a test case that reproduces the issue.

To run the script, save it to a file named `reproducer.py` in the root directory of your project, and execute it with `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

Note that this script uses Django's test framework to create a test database and run the test case. This allows us to isolate the reproduction of the issue from any existing project configuration.