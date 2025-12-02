 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import shutil
from docutils.writers.html4css1 import Writer as HTMLWriter

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def build_sphinx_docs(sphinx_project_dir, build_dir):
    os.chdir(sphinx_project_dir)
    os.system("sphinx-build -b html . {}".format(build_dir))

def check_duplicate_files(build_dir):
    downloads_dir = os.path.join(build_dir, "_downloads")
    if not os.path.exists(downloads_dir):
        return
    files = os.listdir(downloads_dir)
    assert len(files) == 1, "Duplicate files found in {}: {}".format(downloads_dir, files)

def main():
    # Create a simple Sphinx project
    sphinx_project_dir = "sphinx_project"
    os.makedirs(os.path.join(sphinx_project_dir, "document", "downloads"), exist_ok=True)
    with open(os.path.join(sphinx_project_dir, "document", "index.rst"), "w") as index_rst_file:
        index_rst_file.write(":download:`downloads/archive.zip`\n")
        index_rst_file.write(":download:`/document/downloads/archive.zip`\n")
        index_rst_file.write(":download:`../document/downloads/archive.zip`\n")
    with open(os.path.join(sphinx_project_dir, "document", "downloads", "archive.zip"), "wb") as archive_zip_file:
        archive_zip_file.write(b"Archive content")

    # Build Sphinx HTML documentation
    build_dir = "_build"
    build_sphinx_docs(sphinx_project_dir, build_dir)

    # Check for duplicate files
    check_duplicate_files(build_dir)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(2)
    else:
        exit(0)
```
To reproduce the issue, create a directory for the script and the Sphinx project, and then run the script with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.