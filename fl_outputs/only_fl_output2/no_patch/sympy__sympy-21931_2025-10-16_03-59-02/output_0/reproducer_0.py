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

try:
    from sympy.combinatorics.partitions import Partition
    from sympy import FiniteSet

    # First example using a list
    partition_list = Partition([1, 2])
    list_expected_str = "Partition([1, 2])"  # Assuming this is the desired format once the issue is fixed
    actual_list_str = str(partition_list)
    assert actual_list_str == list_expected_str, f"Actual string representation does not match expected for list input. Expected {list_expected_str}, got {actual_list_str}"

    # Second example using a set
    partition_set = Partition({1, 2})
    set_expected_str = "Partition({1, 2})"  # Assuming this is the desired format once the issue is fixed
    actual_set_str = str(partition_set)
    assert actual_set_str == set_expected_str, f"Actual string representation does not match expected for set input. Expected {set_expected_str}, got {actual_set_str}"

except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print("An unexpected error occurred.")
    print_stacktrace(e)
    raise
else:
    print("No issue detected with the printing of `Partition`.")

