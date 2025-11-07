Here is the reproducer script:

```python
from django.db import models

def main():
    class Entity(models.Model):
        id = models.AutoField(primary_key=True)

    class User(Entity):
        pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script defines two Django models, `Entity` and `User`, where `User` inherits from `Entity`. The issue should be reproduced when running this script.