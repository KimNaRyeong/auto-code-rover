import types
from django.conf import settings

def test_settings_configure():
    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        print(settings.foo, settings.baz)  # Should raise an error
        assert False, "Non-uppercase settings should not be allowed"
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, AttributeError), "Expected AttributeError, but got {}".format(type(e))

if __name__ == "__main__":
    test_settings_configure()
