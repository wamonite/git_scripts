#!/usr/bin/env python
"""
git_commit_size.py

Parse a git repository history and return a sorted list of names of
files over 1MB, the size of the file and the commit when they were added.

2013/08/23

Warren Moore
      @wamonite     - twitter
       \_______.com - web
warren____________/ - email
"""

##################################################################
# Imports

import sys
import subprocess
from operator import itemgetter
import shlex

##################################################################
# Constants

MINIMUM_BLOB_SIZE = 1024 * 1024

##################################################################
# Functions

def get_commit_list():
  command_list = shlex.split("git rev-list --all")
  return subprocess.check_output(command_list).splitlines()

def get_commit_blob_list(commit_id):
  command_list = shlex.split("git diff-tree -r -c -M -C --no-commit-id")
  command_list.append(commit_id)
  blob_list = subprocess.check_output(command_list).splitlines()
  return [x.split() for x in blob_list]

def get_blob_size(blob_id):
  command_list = shlex.split("git cat-file -s")
  command_list.append(blob_id)
  return int(subprocess.check_output(command_list).strip())
    
def get_file_size_list():
  commit_list = get_commit_list()
  
  file_list = []
  for commit_id in commit_list:
    blob_list = get_commit_blob_list(commit_id)
    
    for blob_info in blob_list:
      if blob_info[4] == "A":
        try:
          blob_size = get_blob_size(blob_info[3])
          if blob_size > MINIMUM_BLOB_SIZE:
            file_info = (commit_id, blob_info[5], blob_size)
            file_list.append(file_info)
          
        except KeyboardInterrupt:
          raise
        
        except:
          print >> sys.stderr, "Bad blob in commit", commit_id
        
  sorted_file_list = sorted(file_list, key = itemgetter(2), reverse = True)
  
  for file_info in sorted_file_list:
    print "%s,%s,%d" % file_info
    
##################################################################
# Main

if __name__ == "__main__":
  get_file_size_list()
