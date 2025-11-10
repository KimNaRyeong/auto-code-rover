import matplotlib as mpl
from unittest import TestCase

class Reproducer(TestCase):
    def test_matplotlib_deprecation_warning(self):
        try:
            rc = dict(mpl.rc_params())
            mpl.rcParams.update(rc)
            self.fail("MatplotlibDeprecationWarning was expected")
        except MatplotlibDeprecationWarning as e:
            print_stacktrace(e)

if __name__ == "__main__":
    Reproducer().test_matplotlib_deprecation_warning()
