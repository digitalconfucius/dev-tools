#!/usr/bin/env python3

# Usage: 
# Add `# python-script-read-here` to your zshrc file
# Edit zshrc and destination path as needed
# Run python3 copy-zshrc.py
# Push to Github repository

import os

# Expands the '~' to the full path of the user's home directory
home_directory = os.path.expanduser('~')

def copy_lines_from_zshrc():

    zshrc_path = os.path.join(home_directory, '.zshrc')
    destination_path = os.path.join(home_directory, 'Documents/GitHub/dev-tools/.zshrc')  # Update this with the actual destination path and filename

    try:
        with open(zshrc_path, 'r') as zshrc_file:
            lines = zshrc_file.readlines()

        # Find the marker and get all lines after it
        marker = 'python-script-read-here'
        start_copying = False
        lines_to_copy = []
        for line in lines:
            if start_copying:
                lines_to_copy.append(line)
            if marker in line:
                start_copying = True

        # Write the copied lines to the destination file
        with open(destination_path, 'w') as destination_file:
            destination_file.writelines(lines_to_copy)
            
        print("Success.")

    except Exception as e:
        print(f"Error: {e}")

# Run the function
copy_lines_from_zshrc()
