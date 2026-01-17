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


def test_missing_indicator_string_types():
    import numpy as np
    from sklearn.impute import MissingIndicator

    a = np.array([[c] for c in 'abcdea'], dtype=str)
    try:
        result1 = MissingIndicator().fit_transform(a)
        expected_result1 = np.full((6, 1), False, dtype=bool)
        assert np.array_equal(result1, expected_result1), "First check failed with string types."

        result2 = MissingIndicator(missing_values='a').fit_transform(a)
        expected_result2 = np.array([[False], [False], [True], [False], [False], [False]], dtype=bool)
        assert np.array_equal(result2, expected_result2), "Second check failed with string types."

    except Exception as e:
        print_stacktrace(e)
        raise


def test_missing_indicator_object_types():
    import numpy as np
    from sklearn.impute import MissingIndicator

    a = np.array([[c] for c in 'abcdea'], dtype=object)
    try:
        result3 = MissingIndicator().fit_transform(a)
        expected_result3 = np.full((6, 1), False, dtype=bool)
        assert np.array_equal(result3, expected_result3), "First check failed with object types."

        result4 = MissingIndicator(missing_values='a').fit_transform(a)
        expected_result4 = np.array([[False], [False], [True], [False], [False], [False]], dtype=bool)
        assert np.array_equal(result4, expected_result4), "Second check failed with object types."

    except Exception as e:
        print_stacktrace(e)
        raise


if __name__ == "__main__":
    try:
        test_missing_indicator_string_types()
        test_missing_indicator_object_types()
        print("All checks passed successfully.")
    except AssertionError as ae:
        print(f"AssertionError: {ae}")
        exit(1)
    except Exception:
        exit(1)
    else:
        exit(0)
```