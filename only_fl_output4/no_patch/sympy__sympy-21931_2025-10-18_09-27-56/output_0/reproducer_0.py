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

def main():
    from sympy.combinatorics.partitions import Partition
    from sympy import FiniteSet

    # Attempt to reproduce the verbose printing issue
    try:
        partition_list_input = str(Partition([1, 2]))
        partition_set_input = str(Partition({1, 2}))
        
        # Assert that the string representations are not too verbose
        assert partition_list_input == "Partition([1, 2])", "Verbose printing with list input"
        assert partition_set_input == "Partition({1, 2})", "Verbose printing with set input"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if the issue is present

if __name__ == "__main__":
    main()
    print("No issue detected.")
    exit(0)  # Exit with success code if the issue is fixed
