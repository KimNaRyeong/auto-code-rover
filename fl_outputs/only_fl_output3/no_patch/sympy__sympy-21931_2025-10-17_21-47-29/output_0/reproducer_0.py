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

def test_partition_printing():
    from sympy.combinatorics.partitions import Partition
    partition_from_list = Partition([1, 2])
    partition_from_set = Partition({1, 2})

    expected_list_str_format = "Partition([1, 2])"
    expected_set_str_format = "Partition({1, 2})"
    
    assert str(partition_from_list) == expected_list_str_format, f"Expected {expected_list_str_format}, got {str(partition_from_list)}"
    assert str(partition_from_set) == expected_set_str_format, f"Expected {expected_set_str_format}, got {str(partition_from_set)}"

if __name__ == "__main__":
    try:
        test_partition_printing()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Issue not present, exiting with code 0.")
    exit(0)
