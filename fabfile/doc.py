from fabric.api import task, local
import sys

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def view():
    """view the documentation in a browser"""
    local("{browser} doc/build/html/index.html".format(browser=browser))

@task
def html():
    man()
    """build the doc locally and view"""
    local("cd doc; make html")


@task
def gh():
    """deploy the documentation on gh-pages"""
    local("rm -f doc/source/modules/*")
    local("git checkout gh-pages")
    local("make pages")

@task
def man():
    """deploy the documentation on gh-pages"""
    #TODO: match on "Commands"
    local("cm man | grep -A10000 \"Commands\"  | sed \$d  > doc/source/man/man.rst")

    

