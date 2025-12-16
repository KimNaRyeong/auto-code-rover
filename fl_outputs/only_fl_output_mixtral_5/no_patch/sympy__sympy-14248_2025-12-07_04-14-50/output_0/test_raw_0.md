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

    assert actual_str_output == expected_str_output, "The difference of MatrixSymbols does not print as a sum with (-1) coefficient in str printer."
    assert actual_pretty_output == expected_pretty_output, "The difference of MatrixSymbols does not print as a sum with (-1) coefficient in pretty printer."
    assert actual_latex_output == expected_latex_output, "The difference of MatrixSymbols does not print as a sum with (-1) coefficient in latex printer."


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script defines a `main` function that creates two `MatrixSymbol` objects `A` and `B`, and then calculates the difference `A - A*B - B`. It then prints the difference using the `str`, `pprint`, and `latex` functions, and compares the output to the expected output. If the output does not match the expected output, an `AssertionError` is raised. The `print_stacktrace` function is used to print a stack trace when the `AssertionError` is raised.

To run the script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.