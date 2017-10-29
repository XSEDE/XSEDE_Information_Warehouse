#!/bin/bash
PYTHON=/soft/python-current/bin/python
export LD_LIBRARY_PATH=/soft/python-current/lib
export DJANGO_CONF=/soft/warehouse-1.0/conf/settings_info_mgmt.conf
$PYTHON ./manage.py $1 $2 $3 $4 $5
