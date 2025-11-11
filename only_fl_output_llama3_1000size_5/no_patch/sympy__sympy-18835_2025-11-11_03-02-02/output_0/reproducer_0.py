import unittest
from collections import OrderedDict

def uniq(iterable):
    seen = OrderedDict()
    for item in iterable:
        if item not in seen:
            yield item
            seen[item] = None

class TestUniq(unittest.TestCase):

    def test_uniq(self):
        f = list('THISTLE')
        try:
            for i in uniq(f):
                f.remove(i)
                i
        except RuntimeError as e:
            print_stacktrace(e)
            self.fail("uniq modifies list argument")
        else:
            raise AssertionError("Expected RuntimeError")

if __name__ == '__main__':
    unittest.main()
