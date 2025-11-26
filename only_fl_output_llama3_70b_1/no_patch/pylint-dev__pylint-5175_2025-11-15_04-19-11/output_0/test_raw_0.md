Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import pylint.lint as lint
from pylint.reporters import StringReporter

def function(file, *args, sep=";"):
    """Description of the function

    Parameters
    ----------
    file : str
        Path to the input.
    *args
        Relevant parameters.
    sep : str, optional
        File separator.
    """

def main():
    reporter = StringReporter()
    lint.run(['reproducer.py'], reporter=reporter, exit=False)
    output = reporter.out.getvalue()
    if 'W9015: "args" missing in parameter documentation (missing-param-doc)' in output:
        raise AssertionError("Issue is present")
    else:
        print("No warning returned")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```
This script defines the `function` with the same docstring as in the issue description. Then, it runs Pylint on itself using the `lint.run` function and checks if the warning 'W9015: "args" missing in parameter documentation (missing-param-doc)' is present in the output. If the warning is present, it raises an `AssertionError`. If not, it prints a success message.

When you run this script with `python3 reproducer.py`, it should raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.