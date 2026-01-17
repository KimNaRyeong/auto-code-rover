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

def run_sphinx_build(jobs=None):
    cmd = ["sphinx-build", "-n", "-b", "html", "-d", "build/doctrees", "-q", "-E", ".", "build/html"]
    if jobs is not None:  # Add -j option if jobs are specified
        cmd.insert(1, f"-j{jobs}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Sphinx-build failed with return code {result.returncode}.\nStderr: {result.stderr}")
    return result

def get_searchindex_size():
    searchindex_path = "build/html/searchindex.js"
    return os.path.getsize(searchindex_path)

def main():
    try:
        # Clean build directory if exists
        subprocess.run(["rm", "-rf", "build"])
        # Run Sphinx with -j auto
        run_sphinx_build(jobs="auto")
        size_with_j_auto = get_searchindex_size()
        # Clean build directory
        subprocess.run(["rm", "-rf", "build"])
        # Run Sphinx without -j
        run_sphinx_build()
        size_without_j = get_searchindex_size()
        
        assert size_with_j_auto == size_without_j, "Search index sizes do not match."
        print("Issue is fixed!")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code to indicate failure

if __name__ == "__main__":
    main()
```

Explanation:

1. This script first defines a function to print stack traces in a clear format.
2. It then defines `run_sphinx_build` which abstracts running the `sphinx-build` command with and without the `-j auto` option. It accepts an optional `jobs` argument to specify the use of parallel build options.
3. `get_searchindex_size` is a utility function to check the size of the generated `searchindex.js` file, which is used to assert whether the issue exists.
4. The `main` function orchestrates the process: cleaning the build directory, running Sphinx with and without `-j auto`, and then comparing the size of the `searchindex.js` file in both cases. An assertion error is raised if the sizes differ, indicating the issue is present. If no error occurs, it prints a message indicating the issue is fixed.
5. Upon catching exceptions, the script prints a detailed stack trace and exits with a non-zero code to indicate failure.

This script is designed to be placed at the root of the Sphinx project and executed. If the issue exists (the search index size is different with `-j auto`), it will raise an `AssertionError`. If the issue is fixed, it will exit successfully with a message.