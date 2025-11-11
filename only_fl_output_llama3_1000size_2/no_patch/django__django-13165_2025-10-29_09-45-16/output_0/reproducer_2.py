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
        from django.db import models
        class Mallets(models.Model):
            id = models.AutoField(primary_key=True, blank=True, null=True)
            hindsight = models.ForeignKey('Hindsight', models.DO_NOTHING, blank=True, null=True)
            believer = models.IntegerField(blank=True, null=True)
            damnably = models.IntegerField(blank=True, null=True)
            issue = models.IntegerField(blank=True, null=True)
            glover = models.TextField(blank=True, null=True)

        sheer = models.ExpressionWrapper((models.F('issue') / models.F('id')), output_field=models.FloatField())
        lacquer = models.ExpressionWrapper(models.Avg(models.F('sheer'), output_field=models.TextField()), output_field=models.TextField())

        q = Mallets.objects.using('default')
        ret = q.annotate(sheer=sheer).values('sheer').annotate(lacquer=Sum(F('believer'))).order_by('sheer').first()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

if __name__ == "__main__":
    main()
