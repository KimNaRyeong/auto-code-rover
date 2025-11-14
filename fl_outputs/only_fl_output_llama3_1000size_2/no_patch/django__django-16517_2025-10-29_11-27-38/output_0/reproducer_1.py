import os
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, re_path
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.exceptions import AssertionError

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

def reproducer():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

    settings.configure()

    class OrderSearch(LoginRequiredMixin, ListView):
        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

        def get_queryset(self):
            return []

    view = OrderSearch.as_view(template_name='orders.html')

    urlpatterns = [
        re_path(r'^view:orders.views.Orders/$', ViewDetailView.as_view()),
    ]

    try:
        from django.urls import include
        include(urlpatterns)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproducer()
