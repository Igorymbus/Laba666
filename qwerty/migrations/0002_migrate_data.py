from django.db import migrations

def migrate_data(apps, schema_editor):
    # Миграция данных отключена для MySQL
    pass

def reverse_migrate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ("qwerty", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(migrate_data, reverse_migrate),
    ] 
