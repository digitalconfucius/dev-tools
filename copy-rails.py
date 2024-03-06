#!/usr/bin/env python3

# Allows you to copy and rename an existing Rails project.
# Usage: 
# python copy-rails.py /path/to/old/project /path/to/new/project

import os
import shutil
import sys
import re

def copy_rails_project(old_project_dir, new_project_dir):
    old_project_name = os.path.basename(old_project_dir)
    new_project_name = os.path.basename(new_project_dir)

    # Create a new directory for the copied project
    os.makedirs(new_project_dir, exist_ok=True)

    # Copy the contents of the existing project to the new directory, excluding the .git directory
    def ignore_git(dir, files):
        return ['.git'] if '.git' in files else []

    shutil.copytree(old_project_dir, new_project_dir, ignore=ignore_git, dirs_exist_ok=True)

    # Navigate to the new project directory
    os.chdir(new_project_dir)

    # Rename the project in the config/application.rb file
    application_rb_path = "config/application.rb"
    if os.path.exists(application_rb_path):
        with open(application_rb_path, "r") as file:
            content = file.read()
        content = re.sub(r'module\s+(\w+)', f'module {new_project_name.capitalize()}', content)
        with open(application_rb_path, "w") as file:
            file.write(content)
    else:
        print(f"Skipping {application_rb_path} as it doesn't exist.")

    # Update the database configuration in config/database.yml
    database_yml_path = "config/database.yml"
    if os.path.exists(database_yml_path):
        with open(database_yml_path, "r") as file:
            content = file.read()
        content = re.sub(rf'{old_project_name}_(\w+)', rf'{new_project_name}_\1', content)
        with open(database_yml_path, "w") as file:
            file.write(content)
    else:
        print(f"Skipping {database_yml_path} as it doesn't exist.")

    # Update the project name in the config/cable.yml file
    cable_yml_path = "config/cable.yml"
    if os.path.exists(cable_yml_path):
        with open(cable_yml_path, "r") as file:
            content = file.read()
        content = content.replace(old_project_name, new_project_name)
        with open(cable_yml_path, "w") as file:
            file.write(content)
    else:
        print(f"Skipping {cable_yml_path} as it doesn't exist.")

    # Update the session store key in config/initializers/session_store.rb
    session_store_rb_path = "config/initializers/session_store.rb"
    if os.path.exists(session_store_rb_path):
        with open(session_store_rb_path, "r") as file:
            content = file.read()
        content = content.replace(old_project_name, new_project_name)
        with open(session_store_rb_path, "w") as file:
            file.write(content)
    else:
        print(f"Skipping {session_store_rb_path} as it doesn't exist.")

    # Create a new database for the copied project
    os.system("rails db:create")

    # Run any necessary database migrations
    os.system("rails db:migrate")

    # Install the project dependencies
    os.system("bundle install")

    print("Rails project copied and renamed successfully!")

# Check if the required arguments are provided
if len(sys.argv) != 3:
    print("Usage: python copy_rails_project.py <old_project_dir> <new_project_dir>")
    sys.exit(1)

# Get the old and new project directories from the command line arguments
old_project_dir = sys.argv[1]
new_project_dir = sys.argv[2]

# Call the function to copy and rename the Rails project
copy_rails_project(old_project_dir, new_project_dir)