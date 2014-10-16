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

As with all management comments, ensure you are in the appropriate python environment for your site. If you installed Django globally, you should be set. Otherwise, you need to activate the right virtualenv before `./manage.py` will work.

Updates to the "correspondence" spreadsheets
----

Download a CSV from Google Docs or export from Excel; the file must have columns titled `pk` (the primary key of the FEED1 term) and `uri` (the URI/IRI of the FEED2 ontology term). Save this in `al_muscles_correspondence.csv` for muscles or `behavior_correspondence.csv` for behaviors. For example:

```
pk,uri
28,http://purl.obolibrary.org/obo/MFMO_0000002
23,http://purl.obolibrary.org/obo/MFMO_0000009
22,http://purl.obolibrary.org/obo/MFMO_0000324
6,http://purl.obolibrary.org/obo/MFMO_0000073
...
```

You can have other columns in the file if you wish; they will be ignored. You may quote columns with a double-quote `"` and you must separate columns with a comma `,`.

Then run one or both of these commands to import the correspondence(s) and update all legacy data in the DB:

```
./manage.py loadcorrespondence m al_muscles_correspondence.csv
./manage.py loadcorrespondence b behavior_correspondence.csv
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


Looking for FEED1 data which is now missing terms
----

Because the correspondence is incomplete, it is possible that some sensors or trials that had values in FEED1 will be missing values in FEED2. These have to be fixed manually, but you can get a list of them with this command:

```
./manage.py liststuffmissingstuff
```

For example:

```
Trials missing OWL behavior:
  325: awefffffff
      behavior_primary: 'None' pk=0
  /admin/feed/trial/325/
Sensors missing muscle:
  1436: EMG Sensor: 1 (Muscle: None, Side: Left) (EMG)
      location_controlled: 'JEZ Muscle' (pk=54)
  /admin/feed/emgsensor/1436/
  1437: EMG Sensor: 2 (Muscle: None, Side: Left) (EMG)
      location_controlled: 'JEZ Muscle' (pk=54)
  /admin/feed/emgsensor/1437/
  1438: EMG Sensor: 3 (Muscle: None, Side: Left) (EMG)
      location_controlled: 'JEZ Muscle' (pk=54)
  /admin/feed/emgsensor/1438/
```
