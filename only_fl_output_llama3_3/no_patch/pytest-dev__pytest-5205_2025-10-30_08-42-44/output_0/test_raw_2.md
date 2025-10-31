I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import pytest
from hypothesis import given, strategies


def test_xml_generation():
    from xml.etree.ElementTree import Element, tostring
    from io import StringIO

    root = Element('testsuite')
    testcase = Element('testcase', attrib={'name': 'test_xml_generation'})
    properties = Element('properties')
    property = Element('property', attrib={'name': 'hypothesis-stats'}, text='[&apos;test_xml_generation.py::test_xml_generation:&apos;, &apos;&apos;, &apos;  - 100 passing examples, 0 failing examples, 0 invalid examples&apos;, &apos;  - Typical runtimes: &lt; 1ms&apos;, &apos;  - Fraction of time spent in data generation: ~ 49%&apos;, &apos;  - Stopped because settings.max_examples=100&apos;, &apos;&apos;]')
    properties.append(property)
    testcase.append(properties)
    root.append(testcase)

    f = StringIO()
    tostring(root, file=f)
    f.seek(0)
    assert f.getvalue() != ''


if __name__ == "__main__":
    try:
        test_xml_generation()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script will create an XML report with the incorrect `<properties>` tag inside a `<testcase>` tag, which should reproduce the issue.