#!/usr/bin/env python
import os
import sys
from guessb.settings import BASE_DIR
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guessb.settings")
    path= os.path.join(BASE_DIR,  'guessb/dao')
    sys.path.append(path)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
