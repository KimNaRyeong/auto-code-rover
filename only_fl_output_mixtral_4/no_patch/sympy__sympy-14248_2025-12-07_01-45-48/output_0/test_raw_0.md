 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import *
from reproducer import print_stacktrace


def main():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    expected_str_output = "A - A*B - B"
    expected_pretty_output = "A - A*B - B"
    expected_latex_output = "A - A B - B"

    try:
        actual_str_output = str(A - A*B - B)
        actual_pretty_output = pprint(A - A*B - B)
        actual_latex_output = latex(A - A*B - B)

        assert actual_str_output == expected_str_output, "str printer output is incorrect"
        assert actual_pretty_output == expected_pretty_output, "pretty printer output is incorrect"
        assert actual_latex_output == expected_latex_output, "latex printer output is incorrect"
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == "__main__":
    main()
```

This script defines the expected output for each printer and then compares the actual output to the expected output using the `assert` statement. If the assertion fails, an `AssertionError` is raised, and the `print_stacktrace` function is called to print the stack trace. If all assertions pass, the script exits with code 0.