import types
from django.conf import settings

def main():
    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        print(settings.foo, settings.baz)  # Doesn't error
        raise AssertionError("Expected an exception")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()
