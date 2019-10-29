#!/bin/bash

DBHOST=information-warehouse-prod-cluster.cluster-clabf5kcvwmz.us-east-2.rds.amazonaws.com

/usr/pgsql-9.4/bin/pg_dump -h ${DBHOST} -U django_owner -n django -d warehouse \
  >django.dump

/usr/pgsql-9.4/bin/pg_dump -h ${DBHOST} -U xcsr_owner -n xcsr -d warehouse \
  >xcsr.dump

/usr/pgsql-9.4/bin/pg_dump -h ${DBHOST} -U glue2_owner -n glue2 -d warehouse --exclude-table-data=glue2_db_entityhistory \
  >glue2.dump

