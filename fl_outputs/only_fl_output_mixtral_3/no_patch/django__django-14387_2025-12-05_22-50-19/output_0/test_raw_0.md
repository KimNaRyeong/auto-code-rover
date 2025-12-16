 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sqlite3
from django.db import models as db_models
from django.db.models import Q

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Create a test database
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE paiyroll_buss (
                    id INTEGER PRIMARY KEY,
                    jurisdiction TEXT,
                    name TEXT,
                    description TEXT,
                    UNIQUE (jurisdiction, name)
                )''')
cursor.executemany('''INSERT INTO paiyroll_buss (jurisdiction, name, description) VALUES (?, ?, ?)''', [
    ('GB', 'buss1', 'description1'),
    ('GB', 'buss2', 'description2'),
    ('GB', 'buss3', 'description3'),
    ('GB', 'buss4', 'description4'),
    ('GB', 'buss5', 'description5'),
    ('GB', 'buss6', 'description6'),
    ('GB', 'buss7', 'description7'),
    ('GB', 'buss8', 'description8'),
    ('Universal', 'buss9', 'description9'),
    ('Universal', 'buss10', 'description10'),
    ('Universal', 'buss11', 'description11'),
    ('Company', 'buss12', 'description12'),
    ('Company', 'buss13', 'description13'),
    ('Company', 'buss14', 'description14'),
    ('Company', 'buss15', 'description15'),
    ('Company', 'buss16', 'description16'),
    ('Company', 'buss17', 'description17'),
    ('Company', 'buss18', 'description18'),
    ('Company', 'buss19', 'description19'),
    ('Company', 'buss20', 'description20'),
    ('Company', 'buss21', 'description21'),
    ('Company', 'buss22', 'description22'),
    ('Company', 'buss23', 'description23'),
    ('Company', 'buss24', 'description24'),
    ('Company', 'buss25', 'description25'),
    ('Company', 'buss26', 'description26'),
    ('Company', 'buss27', 'description27'),
    ('Company', 'buss28', 'description28'),
    ('Company', 'buss29', 'description29'),
    ('Company', 'buss30', 'description30'),
    ('Company', 'buss31', 'description31'),
    ('Company', 'buss32', 'description32'),
    ('Company', 'buss33', 'description33'),
    ('Company', 'buss34', 'description34'),
    ('Company', 'buss35', 'description35'),
    ('Company', 'buss36', 'description36'),
    ('Company', 'buss37', 'description37'),
])
conn.commit()

# Define the model
class Buss(db_models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = db_models.CharField(max