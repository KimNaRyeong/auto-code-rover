```python
import subprocess
import os
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
    # Create a temporary Jupyter notebook with the required content.
    notebook_content = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sympy as sp\\n",
    "sp.init_printing()\\n",
    "1"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""
    notebook_name = "temp_notebook.ipynb"
    with open(notebook_name, 'w') as notebook_file:
        notebook_file.write(notebook_content)

    try:
        # Attempt to convert the notebook to PDF, catching LaTeX errors.
        process = subprocess.run(["python3", "-m", "nbconvert", notebook_name, "--to", "latex", "--stdout"],
                                 text=True, capture_output=True)
        latex_output = process.stdout

        # Check if the problematic LaTeX code is present.
        if "$$\begin{equation*}" in latex_output and "\end{equation*}$$" in latex_output:
            raise AssertionError("Found problematic LaTeX code that causes bad math environment delimiter error.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Cleanup: Remove the temporary notebook
        if os.path.exists(notebook_name):
            os.remove(notebook_name)

    print("Issue is not present, exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

This standalone Python script, `reproducer.py`, aims to programmatically reproduce the issue where a Jupyter notebook's LaTeX output causes an error when processed by LaTeX due to incorrect math environment delimiters. The script follows these steps:

1. **Creating a Temporary Notebook**: It dynamically creates a temporary Jupyter notebook with the content specified in the provided steps that reproduce the issue.
2. **Conversion Attempt**: It uses the `nbconvert` utility to attempt converting this notebook to LaTeX format, redirecting the output to stdout for analysis.
3. **Checking for Problematic LaTeX Code**: The script then checks for the presence of the problematic LaTeX pattern that was described in the issue (`$$\begin{equation*}` and `\end{equation*}$$`) within the LaTeX output.
4. **Assertion and Stack Trace**: If the problematic code is found, it raises an `AssertionError`, and the custom `print_stacktrace` function is triggered to provide detailed diagnostic information.
5. **Cleanup**: Regardless of the outcome, it ensures to clean up by deleting the temporary notebook to avoid leaving artifacts.
6. **Exit Codes**: It exits with code 0 if the issue is not present (i.e., the problematic LaTeX code was not found in the output), indicating that the issue might have been fixed.

This approach allows for automated testing of the issue's presence in the environment and provides a basis for continuous integration scenarios or automated regression tests.