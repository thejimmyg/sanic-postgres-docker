#!/bin/sh

# Exit if there are any errors
set -e

RETRIES=99

CONNECTION_DATABASE_URL=`echo $DATABASE_URL | sed 's|postgis://|postgres://|'`
until psql "$CONNECTION_DATABASE_URL" -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 2
done
# Exit if we still can't connect after waiting about 200 seconds.
psql "$DATABASE_URL" -c "select 1" > /dev/null
echo "Fixing permissions on /web as `/usr/bin/whoami`"
chown -R `/usr/bin/whoami` /web
echo 'done'
# Just so we know exactly what versions we are using.
pip freeze > /web/freeze.txt
echo "Binding to $PORT"
exec python3 /web/app.py
