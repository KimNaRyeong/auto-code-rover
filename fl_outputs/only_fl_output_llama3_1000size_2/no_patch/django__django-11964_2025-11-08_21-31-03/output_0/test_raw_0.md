Here is the reproducer script:

```python
import django
from django.db import models
from django.utils.translation import gettext_lazy as _

class MyChoice(models.TextChoices):
    FIRST_CHOICE = "first", _("The first choice, it is")
    SECOND_CHOICE = "second", _("The second choice, it is")

class MyObject(models.Model):
    my_str_value = models.CharField(max_length=10, choices=MyChoice.choices)

def main():
    try:
        my_object = MyObject(my_str_value=MyChoice.FIRST_CHOICE)
        print(str(my_object.my_str_value))
        assert str(my_object.my_str_value) == "first"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

To run the script, save it to a file named `reproducer.py` in the root directory of your project and then execute it with `python3 reproducer.py`. This should output the stack trace of the issue.