#!/usr/bin/env python
"""
git_rename_author.py

Script to rename authors and committers over the history of a
repository.

2013/09/11

Warren Moore
      @wamonite     - twitter
       \_______.com - web
warren____________/ - email
"""

##################################################################
# Imports

import sys
import subprocess
import shlex

##################################################################
# Constants

NAME_EMAIL_LOOKUP = {
  "dev": ("A. Developer", "dev@example.com"),
  "test": ("Q.A. Test", "test@example.com")
}

MATCH_NAME_LOOKUP = {
  "dev": "dev",
  "Developer": "dev",
  "test": "test"
}

GIT_COMMAND = """\
git filter-branch -f --env-filter '\
%s\
' --tag-name-filter cat -- --all\
"""

GIT_FILTER_CONDITION = """\
if [ "$GIT_COMMITTER_NAME" = "%(match_name)s" ] || [ "$GIT_AUTHOR_NAME" = "%(match_name)s" ];
then
  export GIT_COMMITTER_NAME="%(name)s";
  export GIT_AUTHOR_NAME="%(name)s";
  export GIT_COMMITTER_EMAIL="%(email)s";
  export GIT_AUTHOR_EMAIL="%(email)s";
fi\
"""

##################################################################
# Functions

def run_rename_command(command):
  command_list = shlex.split(command)
  subprocess.call(command_list)
  
def process_match_list():
  name_list = []
  for match_name, match_key in MATCH_NAME_LOOKUP.iteritems():
    if match_key in NAME_EMAIL_LOOKUP:
      name, email = NAME_EMAIL_LOOKUP[match_key]
      data = {
        "match_name": match_name,
        "name": name,
        "email": email
      }
      
      filter_condition = GIT_FILTER_CONDITION % data
      name_list.append(filter_condition)
  
  command = GIT_COMMAND % "\n".join(name_list)
  run_rename_command(command)

##################################################################
# Main

if __name__ == "__main__":
  process_match_list()
