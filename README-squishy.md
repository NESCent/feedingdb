FEED: a database of mammalian feeding behaviors
====

Servers
----

 * Dev: (in office)
   * http://dev-feed.sqm.private/ 
   * Superuser: `admin` / `admin`
   * Shell: `ssh -p 22421 dev-feed.sqm.private` and `cd /server/feed-django/src; ./manage.py ...`
 * Vagrant: 1.2+
 * Vagrantfile: From `webdev-vagrant` as of June 2014

Notable URLs:

 * http://dev-feed.sqm.private/search/?q=ABCD -- sample search returns all subjects

Create a settings.py
====

TODO: automate this via puppet somehow

Restore database
====
Database `feed`, user `feed`, filename `feed`:

```
dropdb -U feed feed
createdb -U feed feed
pg_restore -d feed -O -U feed feed
```

Create new superuser for testing
====

`./manage.py createsuperuser`

Set password?
====
Figure this out.

Run server
====

```
. ~/venv/bin/activate
cd /server/src/feeddb
./manage.py runserver 0.0.0.0:8000
```
