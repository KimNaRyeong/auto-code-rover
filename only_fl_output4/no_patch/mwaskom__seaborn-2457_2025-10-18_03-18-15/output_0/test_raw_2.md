Given the requirements, here is how you can structure `reproducer.py` to meet the criteria given for reproducing the described issue with seaborn's `lineplot` function, where it should warn and behave differently when `ci=None` is specified. The challenge here involves checking behavior related to how arguments are handled, which isn't directly observable through an exception or typical error message from Python. 

However, for the sake of providing a tangible script as per your request, I'm interpreting the need for an `AssertionError` to indicate the presence of the issue based on the observed behavior as compared to the expected behavior documented or implied by the task description. Since the expected behavior (transformation of arguments or a warning) cannot be directly captured via seaborn's API, the example below will be a bit hypothetical, focusing on triggering an `AssertionError` under the assumption that the actual behavior of seaborn could explicitly be checked in this manner.

```python
import seaborn as sns
import warnings

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

def test_lineplot_ci_behavior():
    # Hypothetically checking if seaborn lineplot warns when ci=None,
    # which is the supposedly correct behavior as per the issue. This code block
    # does not directly capture such behavior, but rather serves as a placeholder
    # for the actual behavioral check.
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sns.lineplot(x=[1, 1, 2, 2], y=[1, 2, 3, 4], ci=None)
        # Assert that a warning was raised about ci=None being ignored or
        # properly handled, which would indicate the current issue is fixed.
        # The following line will thus always raise an AssertionError as it stands,
        # because we are assuming the behavior can be checked and should be fixed.
        assert len(w) > 0 and any("ci=None" in str(warn.message) for warn in w), "Issue with ci=None not warned or handled"

try:
    test_lineplot_ci_behavior()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Indicate test failure due to issue presence
else:
    print("Issue not present or fixed, no AssertionError raised.")
    exit(0)
```

Please note, this script is designed under the hypothetical condition that seaborn's behavior could directly trigger a Python warning or similar observable effect when `ci=None` is incorrectly handled or ignored, which we could capture programmatically. The assertion and warning capture mechanism here does not reflect seaborn's current capabilities but is used illustratively to demonstrate how a test script might respond to the resolved issue.