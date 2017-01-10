#!/bin/bash
PYTHON=/soft/python-2.7.13-2/bin/python
export LD_LIBRARY_PATH=/soft/python-2.7.13-2/lib
export DJANGO_CONF=/soft/warehouse-1.0/conf/settings_info_mgmt.conf
$PYTHON ./manage.py $1 $2 $3 $4 $5
