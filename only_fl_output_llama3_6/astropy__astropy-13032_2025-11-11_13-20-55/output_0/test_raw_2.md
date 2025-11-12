Here is the reproducer script:

```python
import astropy.modeling.bounding_box as bbox_module
from astropy.modeling import models as astropy_models

def test_model_bounding_box_ignored():
    try:
        bbox = bbox_module.ModelBoundingBox((9, 10), astropy_models.Polynomial2D(1), ignored=["x"])
        print(bbox)
        print(bbox.ignored_inputs)
        assert False, "Expected AssertionError"
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_model_bounding_box_ignored()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.