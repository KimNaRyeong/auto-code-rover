Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest
from _pytest.nodes import File, Collection
from _pytest.hookimpl import hookimpl

@pytest.fixture
def test_file():
    return "test_something.py"

@hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session):
    if session.config.getoption("--black"):
        yield File("path/to/non/existent/file", conftest=False)

def main():
    try:
        pytest.main(["-m", "pytest", "--black"])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script creates a test file and then uses the `pytest_collection_modifyitems` hook to add this non-existent file to the collection. This should reproduce the issue.

To run the script, save it in a file named `reproducer.py`, navigate to that directory in your terminal, and execute `python3 reproducer.py`.