 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.contrib import admin
from django.db.models.fields import ArrayField

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = ArrayField(
        models.CharField(max_length=42),
        default=list,
    )

class RelatedModelForm(ModelForm):
    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = ['plop']

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

class ThingAdmin(admin.ModelAdmin):
    inlines = [
        RelatedModelInline
    ]

admin.site.register(Thing, ThingAdmin)

def test():
    admin.site.each_context(request=None)
    request = None
    call_command('makemigrations', 'my_app', interactive=False, no_color=True)
    call_command('migrate', 'my_app', interactive=False, no_color=True)
    admin_site = admin.site
    admin_site.has_requested_index = True
    admin_site.index_template = 'admin/index.html'
    admin_site.app_index_template = 'admin/app_index.html'
    admin_site.site_header = 'Django site admin'
    admin_site.site_title = 'Django administration'
    admin_site.index_title = ''
    admin_site.login_template = None
    admin_site.logout_template = None
    admin_site.password_change_template = None
    admin_site.password_change_done_template = None
    admin_site.password_reset_template = None
    admin_site.password_reset_done_template = None
    admin_site.password_reset_confirm_template = None
    admin_site.password_reset_complete_template = None
    admin_site.opt_in_email_template = None
    admin_site.opt_in_email_html_template = None
    admin_site.opt_out_email_template = None
    admin_site.opt_out_email_html_template = None
    admin_site.opt_in_confirm_email_template = None
    admin_site.opt_in_confirm_email_html_template = None
    admin_site.opt_out_confirm_email_template = None
    admin_site.opt_out_confirm_email_html_template = None
    admin_site.opt_in_cancel_email_template = None
    admin_site.opt_in_cancel_email_html_template = None
    admin_site.opt_out_cancel_email_template = None
    admin_site.opt_out_cancel_email_html_template = None
    admin_site.user_change_password_template = None
    admin_site.user_change_password_done_template = None
    admin_site.user_factory = None
    admin_site.autodiscover()
    app_list = admin_site._build_app_dict(admin_site.get_app_list(), admin_site)
    request = None
    admin_site.each_context(request)
    admin