To accurately reproduce the described issue while abiding by your instructions, we'll craft a `reproducer.py` standalone Python script. This script will generate a simplified project structure mimicking the `pyproject.toml` configuration, including the problematic `ignore-paths` setup. It will then programmatically invoke pylint with the given command options, trying to capture and analyze the output to check if the specified ignore paths are indeed ignored. 

Let's ensure that the script is self-contained, requiring only standard library modules for subprocess management, alongside any necessary file and directory operations. The script will rely on assumptions that Python and pylint are properly installed in the environment where it's being run.

```python
import subprocess
import traceback
import sys
import os

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_project_structure():
    os.makedirs('src/gen', exist_ok=True)
    with open('src/gen/ignored_file.py', 'w') as fp:
        fp.write('# This should be ignored\n')
    with open('pyproject.toml', 'w') as fp:
        fp.write("""
[tool.pylint.MASTER]
ignore-paths = [
  "^src/gen/.*$",
]
""")

def clean_project_structure():
    os.remove('src/gen/ignored_file.py')
    os.remove('pyproject.toml')
    os.rmdir('src/gen')
    os.rmdir('src')

def run_pylint():
    result = subprocess.run(['pylint', '--recursive=y', 'src/'], capture_output=True, text=True)
    return result.stdout + result.stderr

def check_ignore_paths(output):
    if 'ignored_file.py' in output:
        raise AssertionError("Pylint did not ignore the paths specified in ignore-paths.")

def main():
    try:
        setup_project_structure()
        pylint_output = run_pylint()
        check_ignore_paths(pylint_output)
    except Exception as e:
        clean_project_structure()
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issues found. ignore-paths works as expected.")
    finally:
        clean_project_structure()

if __name__ == '__main__':
    main()
```

**Instructions:**

1. Ensure your environment has `pylint` properly installed (`pip install pylint`).
2. Save the above script as `reproducer.py` in the root of your project.
3. Execute the script using Python 3 (`python3 reproducer.py`).

The script creates a basic project structure mimicking the one described in the issue, including a `pyproject.toml` with `ignore-paths` configured to ignore a `src/gen/` directory. It then runs `pylint` with the `--recursive=y` option on this setup to verify whether `pylint` respects the `ignore-paths` configuration. If it finds that pylint incorrectly checks files within the ignored paths, the script will print a stack trace of the AssertionError. Conversely, it will confirm that the issue is fixed if no such files are checked.