# TODO
 - Add time length for songs (NOT FOR VERSION 0.1)
 

# Create venv



# Install requirements

# Setup in Reaper
 - Launch your Reaper DAW
 - Hit Ctrl + P or go to Options > Preferences
 - Navigate to "Control/OSC/web" menu and click "Add"
 - From the "Control surface mode" dropdown menu choose "Web browser interface"
 - Set the web interface port or leave default 8080
 - Optionally set username:password
 - Optionally set the default web interface
 - Copy the Access URL and paste it in your browser - now your Reaper has a web interface.
 - Hit OK in both preference windows

# Execute

 # How to run ui tests

 (venv) python tests/ui/src/test_screenmanagerapp.py


 # how to run business logic tests

 (venv) python -m unittest  