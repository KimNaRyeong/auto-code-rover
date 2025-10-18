```python
# reproducer.py
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

def test_lasso_coef_shape_with_intercept():
    import numpy as np
    from sklearn import linear_model

    est_intercept = linear_model.Lasso(fit_intercept=True)
    est_intercept.fit(np.c_[np.ones(3)], np.ones(3))
    assert est_intercept.coef_.shape == (1,), "Unexpected coef_ shape with intercept"

def test_lasso_coef_shape_without_intercept():
    import numpy as np
    from sklearn import linear_model

    est_no_intercept = linear_model.Lasso(fit_intercept=False)
    est_no_intercept.fit(np.c_[np.ones(3)], np.ones(3))
    assert est_no_intercept.coef_.shape == (1,), "Unexpected coef_ shape without intercept"

if __name__ == "__main__":
    try:
        test_lasso_coef_shape_with_intercept()
        test_lasso_coef_shape_without_intercept()
    except AssertionError as e:
        print_stacktrace(e)
```

- This script first defines a function `print_stacktrace` to print the stack trace of an exception, including the line numbers and the code context for the most recent calls.
- Then, it defines two test functions:
  - `test_lasso_coef_shape_with_intercept` to test the shape of `coef_` with `fit_intercept` set to `True`, which should pass as per the issue's description.
  - `test_lasso_coef_shape_without_intercept` to test the shape of `coef_` with `fit_intercept` set to `False`, where the expected failure (assertion error) demonstrates the issue.
- In the script's main section, it calls these test functions within a try-except block to catch any assertion errors, then prints the stack trace using the previously defined `print_stacktrace` function.
- It should be executed in the root directory of the concerned project (assuming it has scikit-learn and its dependencies installed) by running `python3 reproducer.py`. An `AssertionError` is expected for the second test when the issue is present.