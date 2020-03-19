"""
Title: path file to the repo for executable

Author: Pietro Campolucci
"""

# import packages
import os
import git


# build function to ger directory path
def get_git_root(current_path):
        git_repo = git.Repo(current_path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")

        return git_root, git_repo


# execute
this_path = os.path.dirname(os.path.realpath(__file__))
path = get_git_root(this_path)[0]

# check for debugging
DEBUG = False

if DEBUG:
    print(f"Git root: {get_git_root(this_path)[0]}")
    print(f"Git repo: {get_git_root(this_path)[1]}")
