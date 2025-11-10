Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib import admin
from django.forms.models import ModelForm, ModelChoiceField
from django.test.client import RequestFactory
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = models.CharField(max_length=42)

class RelatedModelForm(ModelForm):
    class Meta:
        model = RelatedModel
        fields = ('plop',)

    def clean(self):
        raise ValidationError("whatever")

class ThingAdmin(admin.ModelAdmin):
    inlines = [admin.TabularInline]

    @property
    def media(self):
        return admin.Media()

def main():
    request_factory = RequestFactory()
    request = request_factory.get('/admin/thing/add/')
    thing_admin = ThingAdmin(model_admin=self)
    inline = RelatedModelInline(admin.TabularInline)
    form = RelatedModelForm(instance=RelatedModel())
    request.POST['plop'] = 'test'
    request.FILES['plop'] = SimpleUploadedFile('test.txt', b'test')
    try:
        thing_admin.save_model(request, None, form, False)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```

This script creates a Django admin interface for the `Thing` model with an inline form for the `RelatedModel`. It then attempts to save the form data and checks if an `AssertionError` is raised, which would indicate that the issue is present. If the error is not raised, it means the issue is fixed.

Please note that this script should be run in a directory where you have a valid Django project set up.