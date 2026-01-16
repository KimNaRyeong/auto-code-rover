# reproducer.py
import os
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_django_environment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    django.setup()

def create_django_settings():
    settings_content = """
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'fake-key'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'myapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'project.urls'
TEMPLATES = []
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
"""
    project_folder = os.path.join(os.getcwd(), "project")
    os.makedirs(project_folder, exist_ok=True)
    settings_path = os.path.join(project_folder, "settings.py")
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings_content)

def create_django_app():
    app_folder = os.path.join(os.getcwd(), "myapp")
    migrations_folder = os.path.join(app_folder, "migrations")
    os.makedirs(migrations_folder, exist_ok=True)
    init_py = os.path.join(migrations_folder, "__init__.py")
    open(init_py, 'a').close() # Create an empty __init__.py

    # models.py
    models_content = """
from django.db import models
class Tag(models.Model):
    name = models.SlugField(help_text="The tag key.")
    value = models.CharField(max_length=150, help_text="The tag value.")
    class Meta:
        ordering = ["name", "value"]
        constraints = [
            models.UniqueConstraint("name", "value", name="unique_name_value"),
        ]
    def __str__(self):
        return f"{self.name}={self.value}"
"""
    models_path = os.path.join(app_folder, "models.py")
    with open(models_path, "w") as models_file:
        models_file.write(models_content)

    # initial migration
    migration_0001_content = """
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(help_text='The tag key.')),
                ('value', models.CharField(help_text='The tag value.', max_length=200)),
            ],
            options={
                'ordering': ['name', 'value'],
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(models.F('name'), models.F('value'), name='unique_name_value'),
        ),
    ]
"""
    migration_0001_path = os.path.join(migrations_folder, "0001_initial.py")
    with open(migration_0001_path, "w") as migration_file:
        migration_file.write(migration_0001_content)

    # second migration which causes the issue
    migration_0002_content = """
from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [('myapp', '0001_initial'),]
    operations = [
        migrations.AlterField(
            model_name='tag',
            name='value',
            field=models.CharField(help_text='The tag value.', max_length=150),
        ),
    ]
"""
    migration_0002_path = os.path.join(migrations_folder, "0002_alter_tag_value.py")
    with open(migration_0002_path, "w") as migration_file:
        migration_file.write(migration_0002_content)

if __name__ == "__main__":
    create_django_settings()
    create_django_app()
    
    setup_django_environment()

    from django.core.management import call_command
    try:
        # Apply migrations
        call_command('migrate')
        print("Migrations applied successfully, issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue present"
