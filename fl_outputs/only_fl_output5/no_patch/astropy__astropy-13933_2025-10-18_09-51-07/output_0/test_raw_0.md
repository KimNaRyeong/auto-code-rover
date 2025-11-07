```python
import astropy.coordinates
import pickle
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_angle_pickling():
    ang = astropy.coordinates.Angle(0.25 * astropy.units.hourangle)
    pang = pickle.loads(pickle.dumps(ang))
    try:
        assert ang.to_string() == pang.to_string(), "Unpickled Angle's to_string does not match original"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Test passed: Unpickled Angle's to_string matches original.")
        sys.exit(0)

if __name__ == "__main__":
    test_angle_pickling()
```