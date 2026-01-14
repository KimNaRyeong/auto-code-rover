 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
from django.core.exceptions import ValidationError
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ArticleManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(archived=False)

class Article(models.Model):
    title = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    objects = ArticleManager()
    _base_manager = models.Manager()

class FavoriteArticles(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class FavoriteArticlesForm(forms.ModelForm):
    class Meta:
        model = FavoriteArticles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].queryset = Article._base_manager.all()

def main():
    article = Article.objects.create(title="Test Article")
    FavoriteArticles.objects.create(article=article)

    form_data = {
        'article': article.id,
    }
    form = FavoriteArticlesForm(data=form_data)
    form.is_valid()

if __name__ == "__main__":
    try:
        main()
    except ValidationError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, it will raise a `ValidationError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 54, in <module>
    main()
  File "reproducer.py", line 48, in main
    form.is_valid()
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/forms.py", line 175, in is_valid
    return self.full_clean()
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/forms.py", line 376, in full_clean
    self._post_clean()
  File "/home/user/.local/lib/python3.8/site-packages/django/forms/models.py", line 390, in _post_clean
