import sys
import runpy
import os
import unittest
from unittest.mock import patch

class TestPylintIssue(unittest.TestCase):

    @patch('runpy.run_module')
    def test_reproducer(self, mock_run_module):
        # Set up the environment to reproduce the issue
        original_path = list(sys.path)
        sys.path.insert(0, "something")

        try:
            runpy.run_module('pylint', run_name="__main__", alter_sys=True)

            # Check if the first item in sys.path is removed
            self.assertEqual(original_path[0], "something")
        except AssertionError as e:
            print_stacktrace(e)
            raise

        finally:
            # Restore the original sys.path
            sys.path = original_path


if __name__ == '__main__':
    unittest.main()
