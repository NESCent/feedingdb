FEED: a database of mammalian feeding behaviors
====

Starting with a prod DB dump (for dev use)
----

To begin working with a DB dump from prod, there a few things you have to do to bring it into the new world. 

First, load the DB dump. Use `vagrant ssh` to log into the box, then restore database `feeddb`, user `feeddb`, filename `feed`:

```
pg_restore -h localhost -d feeddb -O -U feeddb feed
```

Next, you must load the `initial_data` fixture after creating the `MuscleOwl` model but before migrating the `location_controlled` field to `muscle`. Run these commands after loading a prod database dump:

```
./manage.py migrate feed 0058
./manage.py loaddata initial_data
./manage.py migrate feed
```

Then, load the schema and data into Solr:

`sudo feeddb-refresh-solr`

Finally, create a super user with access to edit everything. 

`./manage.py createsuperuser`

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

Create a settings.py
----

TODO: automate this via puppet somehow

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