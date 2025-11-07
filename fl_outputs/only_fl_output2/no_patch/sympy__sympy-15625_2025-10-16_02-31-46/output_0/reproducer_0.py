import json
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

def create_notebook(notebook_name="mynotebook.ipynb"):
    nb_data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sympy as sp\n",
                    "sp.init_printing()\n",
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
                "version": "3.x"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(notebook_name, "w") as f:
        json.dump(nb_data, f)

def convert_notebook_to_pdf(notebook_name="mynotebook.ipynb"):
    process = subprocess.Popen(
        [sys.executable, '-m', 'nbconvert', notebook_name, '--to', 'pdf', '--execute'],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    _, stderr = process.communicate()
    return process.returncode, stderr.decode()

try:
    create_notebook()

    # Convert and check for errors
    returncode, stderr = convert_notebook_to_pdf()
    if returncode != 0 or "LaTeX Error: Bad math environment delimiter." in stderr:
        raise AssertionError("LaTeX conversion issue detected")

    print("Issue not present, converted successfully.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
