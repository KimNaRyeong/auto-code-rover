import os
from django.utils.translation import to_locale

def reproduce_issue():
    try:
        locale = 'nl-nl-x-informal'
        result = to_locale(locale)
        assert result == 'nl_NL_x_informal', "Expected nl_NL_x_informal but got {}".format(result)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
