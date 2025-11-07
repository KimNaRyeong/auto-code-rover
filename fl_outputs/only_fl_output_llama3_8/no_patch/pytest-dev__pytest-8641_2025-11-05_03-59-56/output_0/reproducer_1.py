import logging
from _pytest.logging import ColoredLevelFormatter
import pytest

def test_reproducer():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(funcName)-40.40s L%(lineno)-.4d %(levelname)-5.5s| %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Set the log format string with precision-formatted levelname
    formatter = ColoredLevelFormatter('%(asctime)s %(funcName)-40.40s L%(lineno)-.4d %(levelname)-5.5s| %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        pytest.main(['-v', '-s'])
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Failed to reproduce the issue")
    else:
        raise AssertionError("Failed to reproduce the issue")

if __name__ == '__main__':
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
