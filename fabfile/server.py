from __future__ import with_statement
from fabric.api import task, local, execute, hide,settings
from fabric.contrib.console import confirm
import os
import webbrowser
import platform
import sys

__all__ = ['start', 'kill', 'view', 'clean']

#
# SETTING THE BROWSER BASED ON PLATFORM
#
browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

#
# VERSION MANAGEMENT
#

#
# we are no longer doing version management with the VERSION.txt file,
# but instead including it in setup.py we need to change the code
# here, so do not use the version increment
#

# filename = "VERSION.txt"
# version = open(filename).read()


@task
def kill(server="server"):
    """kills all server processes """
    with settings(warn_only=True):
        with hide('output','running','warnings'):  
            result = local('ps -a | fgrep "python {0}.py" | fgrep -v fgrep'.format(server), capture=True).split("\n")
            for line in result:
                pid = line.split(" ")[0] 
                local("kill -9 {0}".format(pid))

@task
def start(link="inventory",server="server",port="5000"):
    """ starts in dir webgui the program server.py and displays a browser on the given port and link""" 
    kill()
    local("python setup.py install")
    local("cd webui; python {0}.py &".format(server))
    local("sleep 2; {0} http://127.0.0.1:{2}/{1}".format(browser,link,port))

@task
def view(link="inventory"):
    """run the browser"""
    local("sleep 1")
    local("%s http://localhost:5000/%s" % (browser, link))

@task
def clean():
    """clean the directory"""
    local("find . -name \"#*\" -exec rm {} \\;")
    local("find . -name \"*~\" -exec rm {} \\;")
    local("find . -name \"*.pyc\" -exec rm {} \\;")
    local("rm -rf build dist *.egg-info")
    local("rm -rf doc/build ")

