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
    from sympy import symbols, Xor, bool_map

    # Define symbols
    A1, A2 = symbols('A1 A2')

    # Define expressions
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))

    # Checking if the issue is reproducible by evaluating the actual map results
    try:
        map_result_f2_to_f1 = bool_map(f2, f1)
        map_result_f1_to_f2 = bool_map(f1, f2)

        # Validate the result against the expectation
        # The expectation here is based on a correction interpretation of the original issue being that the mapping should not suggest a direct equivalence as f1 and f2 are binary complements, not logically equivalent in terms of configuration.
        if map_result_f2_to_f1 is not None or map_result_f1_to_f2 is not None:
            raise AssertionError("bool_map has incorrectly identified an equivalence between Xor and its negation.")

    except Exception as e:
        print_stacktrace(e)
        raise

    print("Issue successfully reproduced.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print_stacktrace(error)
        exit(1)  # Exit with error code 1 if an AssertionError is caught to indicate the presence of the issue
    except Exception as unexpectedError:
        print_stacktrace(unexpectedError)
        exit(2)  # Exit with error code 2 if any other unexpected exception is caught
    else:
        print("Issue resolved, exiting with code 0.")
        exit(0)  # Exit with code 0 to indicate no exceptions were raised, and the issue has been resolved
