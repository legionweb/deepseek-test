#!/usr/bin/env python
import os
import sys

# Ajout du répertoire courant au path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == "__main__":
    application.run()