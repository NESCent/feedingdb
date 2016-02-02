#!/bin/bash

# This script rebuilds the solr schema from Django, restarts solr, then
# rebuilds the index. This is everything that needs to be done in order to
# synchronize Solr with the Django app.
#
# Takes no arguments, but must be run as root. For example:
#
#   sudo ./feeddb-refresh-solr.sh
#

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Try this:" 1>&2
   echo "sudo $0" 1>&2
   exit 1
fi

set -e


SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

echo "BEGIN building solr schema and restarting solr ..."

source /virtualenv/feeddb/bin/activate
$DIR/../src/manage.py build_solr_schema > /etc/solr/conf/schema.xml 2> /dev/null
service solr restart &> /dev/null

NEXT_WAIT_TIME=0
until curl -s http://localhost:8983/solr/admin/ > /dev/null || [ $NEXT_WAIT_TIME -eq 4 ]; do
   sleep $(( NEXT_WAIT_TIME++ ))
done

echo "END building solr schema and restarting solr"
echo "BEGIN rebuilding solr index ..."

$DIR/../src/manage.py rebuild_index --noinput

echo "END rebuilding solr index"
