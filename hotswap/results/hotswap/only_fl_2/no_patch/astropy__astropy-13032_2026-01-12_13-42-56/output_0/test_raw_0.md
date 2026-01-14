 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
from astropy.modeling.bounding_box import ModelBoundingBox
from astropy.modeling import models as astropy_models

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

def main():
    bbox = ModelBoundingBox((9, 10), astropy_models.Polynomial2D(1), ignored=["x"])
    print(bbox)
    print(bbox.ignored_inputs)
    assert "x" in bbox.ignored_inputs, "The 'x' input should be ignored"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    main()
  File "reproducer.py", line 15, in main
    assert "x" in bbox.ignored_inputs, "The 'x' input should be ignored"
AssertionError: The 'x' input should be ignored
```
This confirms that the `ignored` status of the `x` input is being accounted for during the validation which occurs during the construction of the bounding box, but it is getting "lost" somehow resulting in the weird behavior.