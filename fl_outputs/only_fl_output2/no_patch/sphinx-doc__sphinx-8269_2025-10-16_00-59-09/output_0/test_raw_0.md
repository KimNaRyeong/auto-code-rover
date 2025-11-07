```python
import subprocess
import sys

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

def main():
    try:
        # Step 1: Create a Sphinx project using sphinx-quickstart
        subprocess.run([
            'sphinx-quickstart', '--quiet', '--project', 'proj',
            '--author', 'me', '--release', '1.0', '--language', 'en', '--sep',
            '-p', 'proj', '-a', 'me', '-v', '1.0', '-r', '1.0', '-l', 'en',
            '--makefile', '--batchfile'], check=True)

        # Step 2: Create a document with a broken link
        with open('source/index.rst', 'a') as f:
            f.write('\n`foo <https://google.com/test.txt#test>`_')

        # Step 3: Run linkcheck 
        result = subprocess.run(['make', 'linkcheck'], capture_output=True, text=True)

        # Analyzing the output
        expected_output_not_found = "(line    6) broken    https://google.com/test.txt#test - 404 Client Error: Not Found for url: https://google.com/test.txt"
        actual_output = result.stdout

        # This checks if the actual_output contains the expected error message
        if expected_output_not_found in actual_output:
            print("Issue is fixed")
        else:
            raise AssertionError("Issue is still present. Found output:\n" + result.stdout)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code if there is an exception

if __name__ == "__main__":
    main()
```

This Python script aims to automate the process of reproducing the issue described, following the steps provided closely. When the issue persists, an `AssertionError` is raised with a message detailing the observed output. In contrast, if the specific error message tied to a 404 status is detected in the `linkcheck` output, it concludes that the issue has been resolved. 

For effective issue reproduction and resolution verification, ensure Sphinx and its dependencies are properly installed in your environment. Running this script requires a Python environment where Sphinx's `sphinx-build` and `sphinx-quickstart` commands are accessible.