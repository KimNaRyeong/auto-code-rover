from unittest import TestCase

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

class TestPaginator(TestCase):
    def test_paginator(self):
        class Paginator:
            def page_range(self):
                return [1, 2]

            def __iter__(self):
                for page_num in self.page_range():
                    yield self.page(page_num)

            def page(self, page_num):
                pass

        paginator = Paginator()
        for _ in paginator:
            pass
        assert False, "Paginator should not be iterable"

if __name__ == "__main__":
    try:
        TestPaginator().test_paginator()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
