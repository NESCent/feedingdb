Various "architectural" implementation notes that are worth knowing upfront, 
rather than finding in code comments. 

=== Special SYSTEM user ===

SYSTEM was created by feed data migration 0043, in or after SVN 3649. 
It is intended to be used in data migrations that create new records, 
to fill the "created_by" fields. 

=== Restrictions on Admin's cascaded delete ===

Purpose: Deletion of a term from a CV should not (even with a user confirmation!) lead to deletion 
of associated data objects that have this term in a non-null field.  In other words, a term deletion 
should be permitted only when the term has been replaced by an alternative in all data objects. 

See feed/models.py, the CRITICAL_ASSOCIATED_OBJECTS array. 
TODO: Xianhua, could you explain more how to use this mechanism? 


=== Permissions ===  

The permissions system in FEED extends that of Django 1.1 contrib.auth by adding an ownership check 
to allow an object owner to perform mutating operations that would be blocked by contrib.auth.  
Here are the FEED permission checking rules. 
   To check whether user U has permission P ("add", "change" or "delete") for object O, 
   -  find out the type T of O
   -  if django.auth allows U to do P with T, then FEED allows U do P with O
   -  otherwise, FEED checks whether U is the owner of O; only if so, U can do P with O. 
TODO: Xianhua to put a pointer to the place in code where this happens.   

Individual FEED users do not have individual permissions assigned.  
Instead, we assign users to one of the two groups, which have permissions as follows: 
  - contributors: have "add" permission to all "data" objects (e.g. Study, Sensor, Illustration, ...)
      => a contributor can only change his own "data" objects  
  - terminologists: have "add", "change" and "delete" permissions to all "cv" objects (e.g. Taxon, Units, Behavior)
      => a terminologist can change or delete any "cv" object, even if it was created by another terminologist
    
There is also the "anonymous" group, used for the single user "anonymous".  It is similar to the "contributors" group, 
but the "add" permission is only given on the Bucket and TrialInBucket objects. That is, the anonymous user cannot 
create any data objects, except Buckets and their contents. 

In the interest of uniformity across our multiple instances of FEED, we now try to avoid assigning group permissions via the UI. 
Instead, they are to be assigned in a database migration that introduces a new model type. 
(For the older models, permissions are set properly by the 0048_Group_permissions migration.)
   