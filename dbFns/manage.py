#!/usr/bin/env python
import os
import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    print 'Hello World'
    from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
    




    
