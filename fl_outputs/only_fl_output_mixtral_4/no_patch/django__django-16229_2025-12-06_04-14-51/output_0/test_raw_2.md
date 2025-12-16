 I apologize for the mistake in my previous response. Here's an updated version of the `reproducer.py` file that should reproduce the issue:
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
        fields = '__all__'

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

class ThingAdmin(admin.ModelAdmin):
    inlines = [
        RelatedModelInline
    ]

admin.site.register(Thing, ThingAdmin)

def main():
    class HiddenArrayField(ArrayField):
        def formfield(self, **kwargs):
            defaults = {
                'show_hidden_initial': False,
            }
            defaults.update(kwargs)
            return super().formfield(**defaults)

    class ThingWithHiddenArrayField(Thing):
        plop = HiddenArrayField(
            models.CharField(max_length=42),
            default=list,
        )

    class RelatedModelWithHiddenArrayField(RelatedModel):
        thing = models.ForeignKey(ThingWithHiddenArrayField, on_delete=models.CASCADE)

    class RelatedModelFormWithHiddenArrayField(ModelForm):
        def clean(self):
            raise ValidationError("whatever")

        class Meta:
            model = RelatedModelWithHiddenArrayField
            fields = '__all__'

    class RelatedModelInlineWithHiddenArrayField(admin.TabularInline):
        form = RelatedModelFormWithHiddenArrayField
        model = RelatedModelWithHiddenArrayField
        extra = 1

    class ThingAdminWithHiddenArrayField(admin.ModelAdmin):
        inlines = [
            RelatedModelInlineWithHiddenArrayField
        ]

    admin.site.unregister(Thing)
    admin.site.register(ThingWithHiddenArrayField, ThingAdminWithHiddenArrayField)

    # The following lines will reproduce the issue
    from django.contrib.admin.sites import AdminSite
    admin_site = AdminSite()
    thing = ThingWithHiddenArrayField.objects.create()
    request = None
    response = admin_site.admin_view(ThingAdminWithHiddenArrayField.changeform_view, request, thing.pk)
    if response.context_data['form'].errors:
        print("Issue reproduced:", file=sys.stderr)
        print_stacktrace(response.context_data['form'].errors)
        sys.exit(1)
    else:
        print("Issue not reproduced")
        sys.exit(0)

if __name__ == '__main__':
    main()
```
The changes I made are:

* I added `request = None` to the `admin_site.admin_view` call to provide a request object.
* I changed `object_id=thing.pk` to `thing.pk` to pass the primary key of the `ThingWithHiddenArrayField` object directly.

These changes should allow the