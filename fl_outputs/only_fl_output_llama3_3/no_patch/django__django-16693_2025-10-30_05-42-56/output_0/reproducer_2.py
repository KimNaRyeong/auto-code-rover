def data(request):
    return None

from django.template import Context, Template
import sys
import traceback

try:
    template = Template('''
        {% with data=data %}
            {{ data }}
        {% endwith %}
    ''')
    context = Context()
    template.render(context)
except Exception as e:
    raise AssertionError(f"Expected error, got {e}")
finally:
    print_stacktrace(e)

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        data(None)  # This should raise an error
    except Exception as e:
        raise AssertionError(f"Expected error, got {e}")
    finally:
        print_stacktrace(e)
