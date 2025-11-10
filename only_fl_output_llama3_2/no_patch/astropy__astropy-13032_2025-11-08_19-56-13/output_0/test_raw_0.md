Here is the reproducer script:

```python
import astropy.modeling.bounding_box as bbox_module
from astropy.modeling import models as astropy_models
import pytest

def test_model_bounding_box_ignored():
    try:
        bbox = bbox_module.ModelBoundingBox((9, 10), astropy_models.Polynomial2D(1), ignored=["x"])
        print(bbox)
        print(bbox.ignored_inputs)
        assert False, "Expected AssertionError"
    except AssertionError:
        pass
    else:
        raise AssertionError("ModelBoundingBox with ignored inputs did not raise an error")

if __name__ == "__main__":
    test_model_bounding_box_ignored()
```

This script will run the code that reproduces the issue and check if it raises an `AssertionError`. If it does, then the script will exit with a successful status (0).