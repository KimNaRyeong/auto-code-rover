from django.urls import path, include
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist

def get_object_or_404(model, slug):
    try:
        return model.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise ValueError(f"Object not found: {model.__name__} with slug '{slug}'")

class Account:
    def __init__(self, slug):
        self.slug = slug

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        if isinstance(offer_slug, str):
            offer = get_object_or_404(Account, slug=offer_slug)
        else:
            raise ValueError(f"Expected string, got {type(offer_slug)}")
        return {"offer": offer, "offer_slug": offer_slug}

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
        offer_view = OfferView()
        offer_view.get_context_data(offer_slug=Account("test"))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
