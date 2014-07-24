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

Setting up a server or vagrant box
====

`vagrant provision` will do a lot of the work, but there is some stuff not yet
automated.

Create a settings.py
----

TODO: automate this via puppet somehow

Install & run `solr` with `jetty`
----

You have to manually rerun the `java -jar start.jar` all the time in order to
have search working. The other commands you just do once.

Do this outside of vagrant, in the root of the repo:

```
wget https://archive.apache.org/dist/lucene/solr/3.6.2/apache-solr-3.6.2.tgz
tar xfvz apache-solr-3.6.2.tgz
```

Then log in with `vagrant ssh` and do this:

```
source /virtualenv/feeddb/bin/activate
/server/src/manage.py build_solr_schema > /server/apache-solr-3.6.2/example/solr/conf/schema.xml
cd /server/apache-solr-3.6.2/example
java -jar start.jar
```

You should keep this running as long as you are working with search; if you
change a `search_indexes.py` file, you should rerun the `build_solr_schema`
command.

Restore database
----
Database `feeddb`, user `feeddb`, filename `feed`:

```
pg_restore -h localhost -d feeddb -O -U feeddb feed
```

Create new Django superuser for testing
----

The dev server has a superuser with username `admin` and password `admin. If you load a fresh database dump without a superuser, you can create one with this command:

`./manage.py createsuperuser`

(If you get an error, run `source /virtualenv/feeddb/bin/activate` and try again)
