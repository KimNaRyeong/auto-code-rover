from django.urls import path, re_path
from django.views.generic import TemplateView

def get_object_or_404(cls, slug):
    return cls.objects.get(slug=slug)

class Account:
    objects = None

    def __init__(self, slug):
        self.slug = slug

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        if not isinstance(offer_slug, str):
            print_stacktrace(Exception(f"Expected string, got {type(offer_slug)}"))
            raise AssertionError("Issue present")
        return {"offer": Account("test"), "offer_slug": offer_slug}

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

if __name__ == "__main__":
    try:
        view = OfferView()
        context_data = view.get_context_data(offer_slug=Account("test"))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
