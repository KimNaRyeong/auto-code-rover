Given the stated requirements and based on your previous experiences, it looks like we need a way to programmatically check for the presence of Sphinx and its version, execute the Sphinx build with and without parallelism, and then compare the size of the generated `searchindex.js`. This updated attempt will integrate these steps in a more robust manner to avoid environment-specific issues you encountered, like `sphinx-build` not being found in the PATH when executed in a constrained environment such as through `conda run`.

```python
import subprocess
import os
import sys
import shutil

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_sphinx_build(parallel):
    """Run the Sphinx build process."""
    cmd = [
        sys.executable, "-m", "sphinx",
        "-b", "html",
        "-d", "build/doctrees",
        "-q", "-E",
        ".", "build/html"
    ]
    if parallel:
        cmd.insert(2, "-j")
        cmd.insert(3, "auto")
    
    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)
        searchindex_path = os.path.join("build", "html", "searchindex.js")
        if not os.path.exists(searchindex_path):
            raise FileNotFoundError(f"{searchindex_path} not found")
        return os.path.getsize(searchindex_path)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        print(f"Failed to run Sphinx build. Command: {' '.join(cmd)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        raise

def check_sphinx_installation():
    """Check if Sphinx is installed and return its version."""
    try:
        result = subprocess.run([sys.executable, "-m", "sphinx", "-V"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Sphinx is not available. Please ensure it is installed.") from e

def ensure_clean_build_dir():
    """Ensure a clean start by removing the existing build directory."""
    shutil.rmtree("build", ignore_errors=True)
    os.makedirs("build/html", exist_ok=True)

def main():
    print("Checking Sphinx installation...")
    sphinx_version = check_sphinx_installation()
    print(f"Sphinx version: {sphinx_version}")

    ensure_clean_build_dir()

    print("Running Sphinx build with parallelism...")
    size_with_parallel = run_sphinx_build(parallel=True)

    ensure_clean_build_dir()

    print("Running Sphinx build without parallelism...")
    size_without_parallel = run_sphinx_build(parallel=False)

    print(f"Size with parallel: {size_with_parallel} bytes")
    print(f"Size without parallel: {size_without_parallel} bytes")

    if size_with_parallel >= size_without_parallel:
        print("Issue not present, both search indexes are of comparable size.")
    else:
        print("Issue reproduced: Search index is smaller/wrong with -j auto")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Notes:

- This script checks for the Sphinx installation by attempting to run it as a module. This avoids issues related to the PATH environment variable.
- It uses `sys.executable` to ensure the correct Python interpreter is used to run Sphinx, which can help in environments where multiple Python versions are present or when using virtual environments.
- The script cleans the build directory between runs to ensure that each test starts with the same conditions.
- Rather than raising an `AssertionError`, it prints a clear message and exits with a status code based on the presence of the issue. This makes it more suitable for automated testing environments.
- Ensure this script is placed in the root directory of the Sphinx project, as mentioned.
- Before running the script, make sure Sphinx is installed in the current Python environment (`pip install Sphinx`).