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

def simulate_assertion(byte_value_1, byte_value_2):
    try:
        assert byte_value_1 == byte_value_2
    except AssertionError as e:
        print("Custom AssertionError message to simulate pytest output:")
        diff_msg = f"AssertionError: assert {byte_value_1} == {byte_value_2}\n"
        right_diff = [f"Right contains more items, first extra item: {byte_value_2[0]}" if byte_value_2 else "Right is empty"]
        full_diff = ["-", str(byte_value_1), "+", str(byte_value_2)]
        diff_msg += f"E       {right_diff[0]}\nE       Full diff:\nE       {full_diff}"
        print(diff_msg, file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)

def test_byte_string_comparison():
    # Trying to reproduce the confusing message issue with byte strings
    simulate_assertion(b"", b"42")
    simulate_assertion(b"", b"1")

if __name__ == "__main__":
    test_byte_string_comparison()
