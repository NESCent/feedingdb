This directory contains dumps that are full-DB snapshots (schema+data)
consistent with a particular schema migration in the codebase.

[The reason this directory (../feeddb_snapshots) is outside the
codebase (which is in ../feeddb) is that the snapshots are likely to
grow fairly large, can diverge among installations (e.g., dev vs
prod), and their role is more like additional samples rather than
integral part of the source code.]

File naming convention for the snapshots: 
       nnnn_label.sql
where 
  nnnn  - the migration number for a migration from ../feeddb/feed/migrations
  label - indicates the snapshot source, usually the DB from which the
          snapshot was taken.  Labels are being documented in the list
          below.

This invariant is expected to hold: The database state preserved in
nnnn_label.fmt is consistent with the DB schema after the nnnn
migration.

Consequently, it is generally expected that if someone
  - checks out the app from SVN at the version at which migration nnnn
    was committed, and 
  - loads nnnn_label.sql into a blank DB, 
then the application should run correctly. 

Current snapshot labels: 
 - darwin_feed_dev  -- the feed_dev DB on darwin.nescent.org 


To create a snapshot dump, run 
pg_dump -h myhosturl -U myusername --format plain --no-owner --no-privileges --file nnnn_label.sql mysourcedbname

most likely, 
pg_dump -h darwin.nescent.org -U feeding_app --format plain --no-owner --no-privileges --file NNNN_darwin_feed_dev.sql feed_dev


To load the snapshot into a blank (freshly created) DB, run

psql -d mytargetdbname -U myusername -f NNNN_darwin_feed_dev.sql 


  
