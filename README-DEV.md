# FEED - Instructions for developers

Python dependencies
===================

``dependencies.pip`` lists Python modules on which FeedDB depends.  

The easiest way to satisfy and manage the dependencies is by using
virtualenv and pip.  (virtualenv allows maintaning per-project
installations of python & packages. pip is a package installer, a
replacement of easy_install.  The two tools work well together.)

One-time setup of virtualenv
----------------------------

Install virtualenv: 

    $ easy_install virtualenv  

Create a virtualenv for this project 

    $ virtualenv --no-site-packages ~/pythonvirtualenvs/feeddb

Install the dependencies

    $ source ~/pythonvirtualenvs/feeddb/bin/activate
    src/feeddb$ pip -r dependencies.pip

Working with virtualenv
-----------------------

Activating and deactivating: 

    $ source ~/pythonvirtualenvs/feeddb/bin/activate
    src/feeddb$ deactivate

Installing and removing a package (by its name from pypi.python.org)

    src/feeddb$ pip install PACKAGE_NAME
    src/feeddb$ pip uninstall PACKAGE_NAME

Making a snapshot of the current virtualenv (for placing in SVN)

    src/feeddb$ pip freeze
    src/feeddb$ pip freeze > dependencies.pip

Installing the package list updated by another developer

    src/feeddb$ git checkout master dependencies.pip
    src/feeddb$ pip -r dependencies.pip


Setting up the project in Eclipse with PyDev and EGit
-----------------------------------------------------

The following appears to work: 

- Clone from github, on command line, call the location ``$FEED_GIT_WORK$``
- Create appropriate settings.py in ``$FEED_GIT_WORK$/src/feeddb`` (based on ``settings.py.example``; test with ``./manage.py runserver``)

- Create a PyDev project (in a new or existing workspaces, elsewhere outside of ``$FEED_GIT_WORK$``)
  - For "Project contents", uncheck "Use default" and put in ``$FEED_GIT_WORK$`` for "Directory".  
  - "Grammar Version" == 2.5
  - Uncheck "Create default 'src' folder and add it to the pythonpath?"
  - Note: this will create .project and .pydevproject in ``$FEED_GIT_WORK$``, 
    but they are mentioned in .gitignore and should not be checked into
    the code repository later on 
    (we do not standardize on PyDev as the development tools)  

- Set the source folder in the project
  - In Project Properties (Apple+I), select "PyDev - PYTHONPATH" page
  - On "Source folders" tab, do "Add source folder" and select ``$YOUR_PROJECT/src``

- Tell Eclipse about the git repository
  -  Team... > Share project > Git 
  - This should find and select the .git repository at ``$FEED_GIT_WORK$``
