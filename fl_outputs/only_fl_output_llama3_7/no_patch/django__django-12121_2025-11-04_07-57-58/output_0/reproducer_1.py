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

def main():
    try:
        from django.urls import path, URLPattern
        urlpatterns = [
            path('export/foo/<foo:obj>/', 'index', name='export'),
            path('export/bar/<bar:obj>/', 'index', name='export'),
        ]
        pattern = URLPattern(url='non-matching', name='export')
        print(pattern.url_for('non-matching'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ValueError to be raised")

def index(request):
    pass

if __name__ == '__main__':
    main()
