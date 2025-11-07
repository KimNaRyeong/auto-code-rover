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

def test_issue():
    from sympy.physics.units import Quantity, voltage, current, ohm, convert_to
    vs = Quantity('vs')
    vs.set_dimension(voltage)
    vs_i = Quantity('vs_i')
    vs_i.set_dimension(current)

    expected = ohm  # Expected result
    result = convert_to(vs/vs_i, ohm)  # Actual result

    # Check if the actual result matches the expected result
    assert expected == result, "Division of voltage by current does not yield expected ohm unit."

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)  # Ensure the script exits with a non-zero code on failure
    print("The issue is fixed.")
