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

    actual_str_output = str(A - A*B - B)
    actual_pretty_output = pprint(A - A*B - B)
    actual_latex_output = latex(A - A*B - B)

    assert actual_str_output == expected_str_output, "The str printer does not print the difference of MatrixSymbols as expected."
    assert actual_pretty_output == expected_pretty_output, "The pretty printer does not print the difference of MatrixSymbols as expected."
    assert actual_latex_output == expected_latex_output, "The latex printer does not print the difference of MatrixSymbols as expected."


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script defines a `main` function that creates two `MatrixSymbol` objects `A` and `B`, and then calculates the difference `A - A*B - B`. It then uses the `str`, `pprint`, and `latex` functions to print the difference, and compares the output to the expected output. If the output does not match the expected output, it raises an `AssertionError` with a message indicating which printer did not print the difference as expected. The `print_stacktrace` function is then called to print a stack trace of the error. The script then exits with code 1 to indicate that an error occurred. If the output matches the expected output, the script exits with code 0 to indicate that no errors occurred.