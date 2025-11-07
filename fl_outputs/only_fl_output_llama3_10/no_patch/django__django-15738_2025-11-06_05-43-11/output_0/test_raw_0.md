Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import CommandError
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

django.setup()

class TestReproducer:
    def test_reproducer(self):
        from django.db.models.signals import post_migrate
        from django.db import connection

        # Create the models
        from authors.models import Authors, ProjectDataSet, DataSet, Project

        try:
            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle('authors', verbosity=0)

            migrate_command = MigrateCommand()
            migrate_command.handle(target='authors', verbosity=0)
        except CommandError as e:
            print_stacktrace(e)
            raise AssertionError("Makemigrations and Migrate commands failed")

        try:
            # Create some data
            authors1 = Authors(project_data_set=ProjectDataSet(data_set=DataSet(name='ds1'), project=Project(name='prj1')),
                               state=0, start_date='2022-01-01')
            authors1.save()

            authors2 = Authors(project_data_set=ProjectDataSet(data_set=DataSet(name='ds1'), project=Project(name='prj1')),
                               state=0, start_date='2022-01-01')
            authors2.save()
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError("Integrity error occurred")

        try:
            # Change the field
            from authors.models import Authors

            old_field = Authors._meta.get_field('project_data_set')
            new_field = models.ManyToManyField(ProjectDataSet, related_name='authors')

            Authors._meta.get_field('project_data_set').remote_field = new_field

            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle('authors', verbosity=0)

            migrate_command = MigrateCommand()
            migrate_command.handle(target='authors', verbosity=0)
        except CommandError as e:
            print_stacktrace(e)
            raise AssertionError("Makemigrations and Migrate commands failed")

        if os.path.exists(settings.DATABASES['default']['NAME']):
            connection.close()

if __name__ == '__main__':
    try:
        test = TestReproducer()
        test.test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

print("Test passed")
exit(0)