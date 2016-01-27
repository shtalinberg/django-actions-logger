#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(os.path.abspath(root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
