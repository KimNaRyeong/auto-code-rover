 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import admin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.cache import never_cache

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Define custom admin site
class CustomAdminSite(admin.AdminSite):
    @never_cache
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HTTP Request.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.start_page)

        context = {
            'title': _('Log in'),
            'site_title': self.site_header,
            'site_header': self.site_header,
            'index_title': self.index_title,
            'admin_site': self,
            'app_path': self.name,
            'other_apps': self.get_app_list(),
        }
        context.update(extra_context or {})

        return TemplateResponse(request,
            self.login_template or 'admin/login.html',
            context)

# Define custom model
class CustomModel(models.Model):
    name = models.CharField(max_length=100)
    related_model = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Define custom model admin
class CustomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'related_model')
    readonly_fields = ('related_model',)

# Register custom model with custom admin site
admin_site = CustomAdminSite()
admin_site.register(CustomModel, CustomModelAdmin)

# Generate URL for readonly field
remote_obj = CustomModel.objects.get(id=1)
url_name = 'admin:{}_{}_change'.format(admin_site.name, CustomModel._meta.model_name)
url = reverse(url_name, args=[quote(remote_obj.pk)])

# Check if URL is correct
assert url == '/custom-admin/app/custommodel/1/change/'
```
To reproduce the issue, create a new Django project and add the above code to a file named `reproducer.py` in the root directory of the project. Then run the script using `python3 reproducer.py`. The script should raise an `AssertionError` with the following message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 63, in <module>
    assert url == '/custom-admin/app/custommodel/1/change/'
AssertionError: /admin/app/custommodel/1/change/ != /custom-admin/app/custommodel/1/change/
```
To fix the issue, replace the line that generates the URL with the following code:
```scss
url = reverse(
    url_name,
    args=[quote(remote_obj.pk)],
    current_app=admin_site.name
)
```
After making this change, run the script again using `python3 reproducer.py`. The script should exit with code 0 and not print any error messages.