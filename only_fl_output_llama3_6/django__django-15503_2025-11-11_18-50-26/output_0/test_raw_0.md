Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.test import TestCase, override_settings
from .models import JsonFieldHasKeyTest

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}})
class Reproducer(TestCase):
    def test_json_field_has_key(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 1, "Should have found 1 entry with key '1111'")

    def test_json_field_has_any_keys(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_keys=['foo']).count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_any_keys=['1111']).count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 1, "Should have found 1 entry with key '1111'")

    def test_json_field_has_key(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 0, "Should not have found any entries with key '1111'")

    def test_json_field_has_keys(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_keys=['foo']).count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_keys=['1111']).count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 0, "Should not have found any entries with key '1111'")

    def test_json_field_has_any_keys(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_any_keys=['foo']).count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_any_keys=['1111']).count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 0, "Should not have found any entries with key '1111'")

    def test_json_field_has_key(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        try:
            test2.save()
        except IntegrityError:
            print("IntegrityError: Duplicate key")
            return

        c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()

        self.assertEqual(c1, 1, "Should have found 1 entry with key 'foo'")
        self.assertEqual(c2, 0, "Should not have found any entries with key '1111'")

    def test_json_field_has_keys(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test.save()
        test2 = JsonFieldHasKeyTest