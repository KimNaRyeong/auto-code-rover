Certainly! The following script `reproducer.py` assumes you have a Sphinx project ready to generate the documentation where this script would be located at the project's root. This script will programmatically execute Sphinx to build the documentation and then examine the generated HTML files to verify if the type annotations for properties are correctly cross-referenced.

Given the nature of the reported issue, it's a bit tricky to automatically detect correct cross-referencing in the HTML files without somewhat brittle string searching or HTML parsing, as Sphinx does not directly return this as an error status. Adjustments might be necessary based on your specific documentation structure and Sphinx theme.

```python
import subprocess
import os

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

def check_cross_references(output_dir):
    # Assuming 'index.html' contains the references; adjust as needed.
    target_files = ['index.html']  # Add or modify based on where your references should appear.
    expected_references = ['class_point.html', 'class_rectangle.html', 'class_square.html']  # Adjust the expected references.

    for file_name in target_files:
        try:
            path = os.path.join(output_dir, file_name)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                for reference in expected_references:
                    if reference not in content:
                        raise AssertionError(f"Reference '{reference}' not found in {file_name}")
        except Exception as e:
            print_stacktrace(e)
            exit(1)

def main():
    docs_dir = 'docs'  # Adjust this to your Sphinx documentation root directory, if different.
    output_dir = os.path.join(docs_dir, '_build', 'html')
    try:
        # Change 'make html' to 'sphinx-build . _build/html' if not on Unix-like system
        result = subprocess.run(['make', '-C', docs_dir, 'html'], check=True, capture_output=True, text=True)
        print(result.stdout)
        check_cross_references(output_dir)
        print("Cross-references work as expected.")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script proceeds as follows:

1. It generates the documentation using Sphinx in your specified directory.
2. It checks a predefined list of HTML files for expected cross-reference links.
3. If it does not find the expected references, it raises an `AssertionError` and prints out a stack trace.

Remember, due to the complexity and variability of Sphinx documentation projects, you might need to adjust paths, expected reference strings, and possibly the HTML file names (`target_files` array) where you look for these references.