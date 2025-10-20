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
    try:
        from sympy.combinatorics.partitions import Partition
        partition_list_repr = str(Partition([1, 2]))
        partition_set_repr = str(Partition({1, 2}))

        # Asserting the current behavior is as described in the issue.
        assert partition_list_repr == "Partition(FiniteSet(1, 2))", "Incorrect list representation"
        assert partition_set_repr == "Partition(FiniteSet(1, 2))", "Incorrect set representation"

        # This section should raise an AssertionError if the issue is present
        # And should not raise an error (thus exiting with code 0) once the issue is fixed,
        # assuming the desired behavior is for Partition to print more concisely.

        # Assuming the desired behavior is Partition to be printed without `FiniteSet` for clarity:
        assert partition_list_repr != "Partition(FiniteSet(1, 2))", "Verbose printing not fixed for lists"
        assert partition_set_repr != "Partition(FiniteSet(1, 2))", "Verbose printing not fixed for sets"
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Reraise the assertion error to ensure non-zero exit code if not fixed.

if __name__ == "__main__":
    main()
