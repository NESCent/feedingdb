FEED data
====

This folder contains data used in the FEED database. This file describes how to freshen this data.

Updates to the ontology
----

We must 1) download original ontologies, 2) preprocess to expand indirect relationships, and 3) import terms.  Run in this directory:

```
curl https://feedontology.googlecode.com/svn/trunk/feed.owl > feed.owl
curl https://feedontology.googlecode.com/svn/trunk/FEEDBehavior.owl > FEEDbehavior.owl
.../path/to/feed-ontology-closure feed.owl muscle.closure.owl
.../path/to/feed-ontology-closure FEEDbehavior.owl behavior.closure.owl
```

Then cd to the `src` directory and run the management command to load ontology terms into the database:

```
cd ../src/
./manage.py loadowl m ../data/muscle.closure.owl
./manage.py loadowl b ../data/behavior.closure.owl
```

Updates to the "correspondence" spreadsheets
----

Currently only updates to the Muscle ontology are supported. 

Download a CSV from Google Docs or export from Excel; the file must have columns titled `pk` (the primary key of the FEED1 term) and `uri` (the URI/IRI of the FEED2 ontology term). Save this in `al_muscles_correspondence.csv`. For example:

```
pk,uri
28,http://purl.obolibrary.org/obo/MFMO_0000002
23,http://purl.obolibrary.org/obo/MFMO_0000009
22,http://purl.obolibrary.org/obo/MFMO_0000324
6,http://purl.obolibrary.org/obo/MFMO_0000073
...
```

You can have other columns in the file if you wish; they will be ignored. You may quote columns with a double-quote `"` and you must separate columns with a comma `,`.

Then run this command to import the correspondence and update all data in the DB:

```
./manage.py loadmusclecorrespondence al_muscles_correspondence.csv
```

If the FEED2 term cannot be found for any row, a message is printed showing the `pk` and `uri` value (including blank `uri` values). For example, this is a normal import with six unmigrated terms:

```
No match for 44: 
No match for 54: 
No match for 38: 
No match for 4: 
No match for 31: 
No match for 29: 
```
