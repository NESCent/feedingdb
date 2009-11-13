 ------------------------------------
|                configuration                                  |
\________________________________________/ 
(need more work here )
1. data base
2. media root
3. static root
4. and so on 


------------------------------------
|                third-party django modules           |
\________________________________________/ 

1. django-pagination

Project website: 
    http://code.google.com/p/django-pagination/

Installing the latest development version of django-pagination
---------------------------------------------------------------

To install, first check out the latest version of the application from
subversion:

    svn co http://django-pagination.googlecode.com/svn/trunk django-pagination

Now, link the inner ``pagination`` project to your Python path:

    sudo ln -s `pwd`/pagination SITE_PACKAGES_DIR/pagination

If you don't know the location of your site packages directory, this hack might
do the trick for you:

    sudo ln -s `pwd`/pagination `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/pagination
    
Now it's installed!  Please see usage.txt for information on how to use this
application in your projects.

Installing via setup.py
-----------------------

Included with this application is a file named ``setup.py``.  It's possible to
use this file to install this application to your system, by invoking the
following command:

    sudo python setup.py install

Once that's done, you should be able to begin using django-pagination at will.

Installing via setuptools
-------------------------

If you have setuptools_ installed, you can simply run the following command
to install django-pagination:

    sudo easy_install django-pagination

.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools

 ------------------------------------
|                other supporting modules           |
\________________________________________/ 

1. jquery

Project website:
   http://jquery.com/
  
2. jquery checkbox toggle
Project website:
    http://www.texotela.co.uk/code/jquery/checkboxes/
 
