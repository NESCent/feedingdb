Search is done with Haystack and Solr
====

We implement search by building upon the great work of Haystack and Solr. The heavy lifting is done by Solr; Haystack provides a nice Python API for working with search queries, forms, and views.

Prerequisites
----

In order for search to work, you must:
 * Be running solr on the host & port specified in `HAYSTACK_CONNECTIONS`, by running `cd /server/apache-solr-xxx/example; java -jar start.jar`
 * Run `./manage.py rebuild_index --noinput` when changing indexing templates or data
 * Run `./manage.py build_solr_schema > /server/apache-solr-xxx/example/solr/conf/schema.xml` when modifying search schema (`search_indexes.py`)
 * Restart `solr` after `build_solr_schema`

Adding fields (via `text` field, no boost)
----

This is easy. To add a searchable field, concatenate it with the other search text by editing `src/feeddb/feed/templates/search/indexes/feed/trial_text.txt`. Use standard Django template syntax; the `object` variable is the trial object.

This method does not allow us to specify a boost for the field and there is no way to control, at query time, whether the search will match that field.

Adding fields (via its own field, optional boost)
----

This is harder, but provides more options. Steps:

 * Add the field to `search_indexes.py` in the appropriate search index
 * Edit `forms.py` to add a `filter_or(...)` on the `sqs` for the desired field
 
In some future version, we might expose this on the front end to allow users to target their search to specific fields. In addition, we might be able to know which fields our query matched.
