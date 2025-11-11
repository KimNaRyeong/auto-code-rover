Here is the reproducer script:

```python
import django
from django.db.models import Value, IntegerField
from django.test import TestCase
from your_app.models import Sample  # Replace 'your_app' with your actual app name

django.setup()

class Reproducer(TestCase):
    def test_union_annotated_diff_distinct(self):
        user = self.get_or_create_admin_user()
        Sample.h.create(user, name="Sam1")
        Sample.h.create(user, name="Sam2 acid")
        Sample.h.create(user, name="Sam3")
        Sample.h.create(user, name="Sam4 acid")
        Sample.h.create(user, name="Dub")
        Sample.h.create(user, name="Dub")
        Sample.h.create(user, name="Dub")
        self.user = user

        qs = Sample.objects.filter(user=self.user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
        self.assertEqual(qs.count(), 2)  # This assertion should raise an AssertionError

try:
    Reproducer().test_union_annotated_diff_distinct()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced. It seems the issue is fixed.")
exit(0)
```

Replace `'your_app'` with your actual app name in `from your_app.models import Sample`.