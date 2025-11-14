import types
from django.conf import settings

def test_settings_configure():
    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        assert settings.foo == "bar"
        assert settings.baz == "qux"
        raise AssertionError("Non-uppercase settings were allowed in settings.configure()")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_settings_configure()
    print("Issue is fixed, exiting with code 0")
    sys.exit(0)
