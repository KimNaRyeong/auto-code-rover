Given the feedback and requirement for a standalone Python script that does not depend on the external Sphinx command line tool, the revised approach is to utilize the Sphinx Python API directly to initiate the build process. This approach ensures the script is self-contained and only relies on the Python environment where Sphinx is installed as a library.

This script also takes into account the feedback regarding the 'sphinx-build' command not being found, by not relying on any external command execution. Instead, it uses Sphinx's Python API to programmatically build the documentation, which should address the issue of finding and executing the `sphinx-build` binary.

Here is a revised version of the script:

```python
import os
from sphinx.application import Sphinx
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

def check_svg_links(base_url, svg_file, expected_links):
    namespace = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
    tree = ET.parse(svg_file)
    root = tree.getroot()
    links = root.findall('.//svg:a', namespace)
    actual_links = [link.get('{http://www.w3.org/1999/xlink}href') for link in links]

    for expected in expected_links:
        full_expected = urljoin(base_url, expected)
        if full_expected not in actual_links:
            raise AssertionError(f"Link {full_expected} not found in SVG file")

def build_sphinx_docs(source_dir='docs_source', build_dir='build', buildername='html'):
    app = Sphinx(
        srcdir=source_dir,
        confdir=source_dir,
        outdir=os.path.join(build_dir, buildername),
        doctreedir=os.path.join(build_dir, "doctrees"),
        buildername=buildername,
    )
    app.build(force_all=True)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    build_dir = 'docs_build'
    base_url = 'http://example.com/docs_build/'  # This is a placeholder URL
    svg_file = os.path.join(build_dir, 'html', 'my_package', 'index.svg')  # Adjust according to actual SVG location
    expected_links = [
        'my_package/my_class_1.html#my_package.MyClass1',
        'my_package/my_class_2.html#my_package.MyClass2'
    ]

    try:
        build_sphinx_docs()
        check_svg_links(base_url, svg_file, expected_links)
        print("Success: All links are correct.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

**Notes and Adjustments Required:**
- **Sphinx API:** This script uses Sphinx's internal API to initiate the build. Ensure Sphinx is installed in the environment where this script runs.
- **Paths:** You might need to adjust paths for the source directory, build directory, and the SVG file according to your project's layout.
- **Base URL:** The `base_url` variable is used to form the full expected URLs for comparison. Adjust it to match your actual setup or testing scenario.

This script omits external command execution and directly leverages the Python API provided by Sphinx, thereby ensuring compatibility and avoiding the issue related to the execution of `sphinx-build`.