To create a Python script that replicates the reported Sphinx issue and incorporates the provided functionality for printing stack traces, follow the structure laid out below. This script will attempt to build your Sphinx documentation twice: first without the `-j auto` option and then with it. It will compare the sizes of `searchindex.js` from both builds to verify if the problem occurs, raising an `AssertionError` if the issue is present (i.e., the search index is considerably smaller when built with `-j auto`).

```python
import subprocess
import os
import shutil

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

def sphinx_build(jobs=None):
    command = ['sphinx-build']
    if jobs is not None:
        command.extend(['-j', jobs])
    command.extend([
        '-n', '-b', 'html', '-d', 'build/doctrees', '-q', '-E', '.', 'build/html'
    ])
    subprocess.run(command, check=True)

def get_searchindex_size():
    try:
        return os.path.getsize('build/html/searchindex.js')
    except FileNotFoundError as e:
        print_stacktrace(e)
        raise

def main():
    initial_dir = os.getcwd()
    try:
        # Make sure we start with a clean state
        if os.path.exists('build/html'):
            shutil.rmtree('build/html')

        # Run Sphinx without -j, record the searchindex.js size
        sphinx_build()
        size_without_j = get_searchindex_size()

        # Clean up before the next run
        shutil.rmtree('build/html')

        # Run Sphinx with -j auto, record the searchindex.js size
        sphinx_build(jobs='auto')
        size_with_j = get_searchindex_size()

        # Compare the sizes to determine if the issue exists
        if size_with_j < size_without_j:
            raise AssertionError("searchindex.js is smaller with `-j auto` indicating a potential issue.")

        print("No issue detected: searchindex.js sizes are consistent.")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        os.chdir(initial_dir)

if __name__ == "__main__":
    main()
```

Please ensure that this script is executed in the root directory of your Sphinx project, where your `conf.py` file is located. This directory should also be prepared such that executing the `sphinx-build` commands can successfully generate the documentation.

**Pre-requisites:**

- Sphinx must be installed in your Python environment (`pip install sphinx`).
- The current working directory must be the root of a Sphinx project.
- The Sphinx project must be configured correctly and able to be built without errors under normal circumstances.

**How It Works:**

1. The script starts by ensuring there's no pre-existing build at `build/html`. If there is, it removes it to start fresh.
2. It runs the `sphinx-build` command twice, once without the `-j` option and once with `-j auto`, each time deleting the `build/html` directory in-between to ensure a clean environment for each build.
3. After each build, it checks the size of the `searchindex.js` file. If the size is smaller when built with `-j auto`, the script treats this as a replication of the reported issue, raises an `AssertionError`, and provides a detailed traceback.
4. It finally cleans up by returning to the initial directory where the script was run, and exits with an error code if an issue was detected.

If the script exits without any errors and prints "No issue detected", then under the conditions tested, the issue does not replicate. Otherwise, it provides detailed output for debugging the problem.