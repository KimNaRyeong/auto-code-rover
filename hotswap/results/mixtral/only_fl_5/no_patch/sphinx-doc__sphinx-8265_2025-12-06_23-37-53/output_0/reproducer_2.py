import sys
import traceback
import inspect

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyClass:
    def __init__(self):
        pass

    def add_lines(self, lines, color=(1, 1, 1), width=5, label=None, name=None):
        pass

if __name__ == '__main__':
    my_obj = MyClass()
    argspec = inspect.getargspec(my_obj.add_lines)
    args = argspec.args[1:]
    defaults = argspec.defaults
    default_args = dict(zip(args[-len(defaults):], defaults))
    html_code = '''
    <dl class="function">
      <dt id="add-lines">
        <span class="function-name">add_lines</span>
        <span class="argspec">(<span class="arg">lines</span>, <span class="optional">color=<span class="default">1</span>, <span class="optional">1</span>, <span class="optional">1</span></span>, <span class="optional">width=<span class="default">5</span></span>, <span class="optional">label=<span class="default">None</span></span>, <span class="optional">name=<span class="default">None</span></span>)</span>
      </dt>
      <dd><p>Add lines to the plot.</p>
      </dd>
    </dl>
    '''
    parsed_args = [x.strip() for x in html_code.split('color=')[1].split(',')[:3]]
    parsed_defaults = [str(x) for x in list(default_args.values())[:3]]
    for parsed_arg, parsed_default in zip(parsed_args, parsed_defaults):
        if parsed_arg != parsed_default:
            raise AssertionError(f'Argument default value is incorrectly parsed as {parsed_arg} instead of {parsed_default}')
