import os
import sys
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyperion.settings")
django.setup()

sys.stdout.reconfigure(encoding="utf-8")
call_command("inspectdb", database="zip_db")
