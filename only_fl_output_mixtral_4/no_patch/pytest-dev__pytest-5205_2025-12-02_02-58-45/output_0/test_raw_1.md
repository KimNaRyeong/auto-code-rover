 Here's a standalone Python script `reproducer.py` that reproduces the issue:

```python
import xml.etree.ElementTree as ET
import unittest
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestXMLGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="0" name="pytest" skipped="0" tests="1" time="0.211"''' \
                      '''>''' \
                      '''    <testcase classname="test_xml_generation" file="test_xml_generation.py" line="3" name="test_xml_generation"''' \
                      '''              time="0.074"''' \
                      '''    >''' \
                      '''        <properties>''' \
                      '''            <property name="hypothesis-stats"''' \
                      '''                      value="[&apos;test_xml_generation.py::test_xml_generation:&apos;, &apos;&apos;, &apos;  - 100 passing examples, 0 failing examples, 0 invalid examples&apos;, &apos;  - Typical runtimes: &lt; 1ms&apos;, &apos;  - Fraction of time spent in data generation: ~ 49%&apos;, &apos;  - Stopped because settings.max_examples=100&apos;, &apos;&apos;]"/>''' \
                      '''        </properties>''' \
                      '''    </testcase>''' \
                      '''</testsuite>'''

        cls.root = ET.fromstring(cls.xml_content)

    def test_xml_generation(self):
        for testcase in self.root.iter('testcase'):
            if 'properties' in testcase.attrib:
                del testcase.attrib['properties']

        for properties in self.root.iter('properties'):
            self.root.remove(properties)

        # Add properties to testsuite
        properties = ET.SubElement(self.root, 'properties')
        property_element = ET.SubElement(properties, 'property')
        property_element.attrib['name'] = 'hypothesis-stats'
        property_element.attrib['value'] = 'some-value'

        output = ET.tostring(self.root, encoding='unicode', xml_declaration=True)
        expected = '''<?xml version='1.0' encoding='utf-8'?>
<testsuite errors="0" failures="0" name="pytest" skipped="0" tests="1" time="0.211"''' \
                  '''>''' \
                  '''    <testcase classname="test_xml_generation" file="test_xml_generation.py" line="3" name="test_xml_generation"''' \
                  '''              time="0.074"''' \
                  '''    />''' \
                  '''    <properties>''' \
                  '''        <property name="hypothesis-stats" value="some-value"/>''' \
                  '''    </properties>''' \
                  '''</testsuite>'''

        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
```

To run the script, execute `python3 reproducer.py`. The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should exit with code 0 when the issue