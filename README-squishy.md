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
