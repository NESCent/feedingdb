Restore database
====
Database `feed`, user `feed`, filename `feed:

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
