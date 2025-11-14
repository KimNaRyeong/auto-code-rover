Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import logging
import pytest

def _check_cond():
    logging.warning("_check_cond")
    return True


@pytest.mark.skipif(not _check_cond(), reason="_check_cond not met")
def test_logging():
    logging.warning("Schmift")


try:
    import sys
    if __name__ == "__main__":
        from _pytest.config.argparsing import final_configurator
        from _pytest.config import ExitCode

        def get_pytest_config(config):
            return config

        configurator = final_configurator(hook=final_configurator.hook)
        config = configurator(constructor=get_pytest_config)

        test_logging()
except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script should reproduce the issue when run with `python3 reproducer.py`.