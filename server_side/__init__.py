"""
All server side code is located in this package.
Provides a working_dir variable to ensure that the files loaded
and created doesn't depend on the current working directory.
"""
import os
__working_dir__: str = os.path.dirname(os.path.abspath(__file__))  # the server_side directory's absolute path
