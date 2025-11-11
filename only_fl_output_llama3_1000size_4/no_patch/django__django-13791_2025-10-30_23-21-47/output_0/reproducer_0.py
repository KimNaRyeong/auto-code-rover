import datetime
from django.utils import dateparse

def duration_iso_string(td):
    days = td.days
    if days < 0:
        sign = '-'
    else:
        sign = '+'

    return f'{sign}P{abs(days)}DT00H00M00S'

def reproduce_issue():
    try:
        td = datetime.timedelta(days=-1)
        duration_str = duration_iso_string(td)
        result = dateparse.parse_duration(duration_str)
        assert result.days == -1, "Expected days to be -1"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
