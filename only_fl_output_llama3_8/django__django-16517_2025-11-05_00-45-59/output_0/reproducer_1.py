import os
from django.conf import settings
from django.contrib.admindocs.views import ViewDetailView
from django.core.exceptions import AssertionError
from django.urls import path, re_path
from django.views.generic import ListView

settings.configure()

class OrderSearch(LoginRequiredMixin, UserPassesTestMixin, ListView):
    pass

def view_detail(request, view_name):
    try:
        ViewDetailView._get_view_func(view_name)
    except Exception as e:
        raise AssertionError("Issue reproduced") from e

re_path(r'view:(?P<view_name>\w+)', view_detail)

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    try:
        ViewDetailView.as_view()(None, 'view:orders.views.Orders')
    except Exception as e:
        print_stacktrace(e)
        exit(1)
