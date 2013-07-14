#!/bin/bash
#
# Run pylint on all .py files in the current directory.
#   Output to doc/pylint/filename.html
# Don't bother if the source file hasn't been updated since last run.

mkdir -p doc/pylint

for x in webui/*.py; do
    if [[ $x -nt doc/pylint/$x.html ]]; then
        echo "Running pylint on $x ..."
        pylint --html=y $x > doc/pylint/$x.html
    else
        echo "Don't need to run pylint on $x."
    fi
 done
echo "Done."
