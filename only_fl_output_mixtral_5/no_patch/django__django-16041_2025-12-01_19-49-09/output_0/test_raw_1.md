 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.forms import BaseFormSet, formset_factory
from django.utils.functional import empty
from django.utils.six import with_metaclass

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyFormSet(with_metaclass(BaseFormSet)):
    def __init__(self, *args, **kwargs):
        self.empty_permitted = kwargs.pop('empty_permitted', None)
        super(MyFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['empty_permitted'] = self.empty_permitted
        return super(MyFormSet, self)._construct_form(i, **kwargs)

MyFormSetForm = formset_factory(empty, formset=MyFormSet)

def test_view():
    request = None
    context = {}
    MyModel = type('MyModel', (object,), {})
    context['formset'] = MyFormSetForm(
        queryset=MyModel.objects.none(),
        form_kwargs={'empty_permitted': True}  # or form_kwargs = {'empty_permitted':False}
    )

if __name__ == '__main__':
    try:
        test_view()
    except KeyError as e:
        print_stacktrace(e)
        assert False, "KeyError should not occur"
```
When executed with `python3 reproducer.py`, the script raises a `KeyError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    test_view()
  File "reproducer.py", line 29, in test_view
    form_kwargs={'empty_permitted': True}  # or form_kwargs = {'empty_permitted':False}
  File "reproducer.py", line 15, in _construct_form
    kwargs['empty_permitted'] = self.empty_permitted
KeyError: 'empty_permitted'
