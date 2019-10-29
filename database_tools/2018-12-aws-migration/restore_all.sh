#!/bin/bash

RDS=information-warehouse-prod-cluster.cluster-clabf5kcvwmz.us-east-2.rds.amazonaws.com

#zcat django.dump.gz | \
#  psql -h ${RDS} -U django_owner -d warehouse -f -

#zcat xcsr.dump.gz | \
#  psql -h ${RDS} -U xcsr_owner   -d warehouse -f -

zcat glue2.dump.gz | \
  psql -h ${RDS} -U glue2_owner  -d warehouse -f -
