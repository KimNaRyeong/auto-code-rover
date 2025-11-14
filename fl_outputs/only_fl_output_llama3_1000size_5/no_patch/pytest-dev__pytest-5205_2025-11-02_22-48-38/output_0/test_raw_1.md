I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
import pytest
from hypothesis import given, strategies

def test_xml_generation():
    @given(x=strategies.integers(1, 10))
    def inner_test_xml_generation(x):
        assert 1 <= x <= 10

if __name__ == "__main__":
    try:
        pytest.main(["--junitxml=report.xml", "-v"])
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script should be run with `python3 reproducer.py` and it will reproduce the issue.