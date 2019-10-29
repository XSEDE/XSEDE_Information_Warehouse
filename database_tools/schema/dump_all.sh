#!/bin/bash -x
pg_dumpall --roles-only -U postgres -f roles_raw.sql
pg_dump -U postgres warehouse -f warehouse_raw.sql -s -n glue2 -t 'glue2.*'
