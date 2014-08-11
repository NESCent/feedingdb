FEED: a database of mammalian feeding behaviors
====

Starting with a prod DB dump (for dev use)
----

To begin working with a DB dump from prod, there a few things you have to do to bring it into the new world. 

First, load the DB dump. Use `vagrant ssh` to log into the box, then restore database `feeddb`, user `feeddb`, filename `feed`:

```
pg_restore -h localhost -d feeddb -O -U feeddb feed
```

Enter `feeddb` when prompted for a password. You will see errors like this; it is OK:

```
GRANT ALL ON TABLE feed_trial T...
pg_restore: [archiver (db)] Error from TOC entry 2667; 0 0 ACL feed_trial_id_seq feeding_app
pg_restore: [archiver (db)] could not execute query: ERROR:  role "feeding_app" does not exist
    Command was: REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM feeding_app;
GRANT ALL O...
WARNING: errors ignored on restore: 75
```

If instead you see several hundred errors, something else has gone wrong.

Next, you must dance a little jig in order to load muscle terms and run a dumb data migration to get some data to play with. Run these commands after loading a prod database dump:

```
./manage.py migrate feed
./manage.py migrate feed 0058
./manage.py migrate feed
```

Then, load the schema and data into Solr:

`sudo feeddb-refresh-solr`

Finally, create a super user with access to edit everything. 

`./manage.py createsuperuser`

Correspondence of FEED1 AnatomicalLocation and FEED2 Muscles
----

The [canonical correspondence](https://docs.google.com/a/squishymedia.com/spreadsheets/d/1CU8Gw7ukyt0q4AHRAJ6b5HgrNukjALCVTdlQ-7dgABI/edit#gid=0) is a Google Doc accessible by both Squishy and the client representatives. The latest CSV export of that spreadsheet should be kept in `data/al_muscles_correspondence.csv`. After updating that file from the Google Doc, you can load the correspondence into the database with this command:

```
./manage.py loadmusclecorrespondence ../data/al_muscles_correspondence.csv
```

Then you need to rerun the migration.

```
./manage.py migrate feed 0066
./manage.py migrate feed
```

Fixtures for Behavior and Muscle
----

Behavior and Muscle terms have been loaded from a pre-reasoned OWL file and saved to the `initial_data.yaml` file. Usually this is fine, but if you want to load new terms from the OWL files, you have to repeat the process below.

Load data from OWL file:

```
./manage.py loadowl m .../muscle-closure.owl
./manage.py loadowl b .../behavior-closure.owl
```

If it looks good, save it to the fixtures -- this gets reloaded on every migration.

```
./manage.py dumpdata --format yaml feed.MuscleOwl feed.BehaviorOwl > feeddb/feed/fixtures/initial_data.yaml
```

Servers
----

 * Dev: (in office)
   * http://dev-feed.sqm.private/ 
   * Superuser: `admin` / `admin`
   * Shell: `ssh -p 22421 dev-feed.sqm.private` and `./manage.py ...`
 * Vagrant: 1.2+
 * Vagrantfile: From `webdev-vagrant` as of June 2014

Notable URLs:

 * http://dev-feed.sqm.private/search/?q=pig -- sample search

Setting up a server or vagrant box
====

`vagrant provision` will do a lot of the work, but there is some stuff not yet
automated.


Refresh solr schema & index
====

This is now automated via puppet configuration. See `vagrant/manifests/default.pp` for details.

If you make changes to the schema or want to rebuild the index, run:

```
# while inside vagrant or on the dev server:
sudo feeddb-refresh-solr
# while outside vagrant:
vagrant ssh -c sudo feeddb-refresh-solr
```

If you know you haven't changed the index schema, you can do a simple index rebuild like this:

```
./manage.py rebuild_index --noinput
```
