#!/bin/bash

/usr/pgsql-9.4/bin/pg_dump -U django_owner -n django -d warehouse \
  >django.dump

/usr/pgsql-9.4/bin/pg_dump -U xcsr_owner -n xcsr -d warehouse \
  >xcsr.dump

#/usr/pgsql-9.4/bin/pg_dump -U glue2_owner -n glue2 -d warehouse --exclude-table-data=glue2_db_entityhistory \

/usr/pgsql-9.4/bin/pg_dump -U glue2_owner -n glue2 -d warehouse \
  >glue2.dump
