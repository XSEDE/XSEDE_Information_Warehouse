#!/bin/bash
# This script was written to run on info3 as the software user
LD_LIBRARY_PATH=/soft/python/python-3.6.8-base/lib
export LD_LIBRARY_PATH

source /soft/python-pipenv/awscli-SyGJgF6m/bin/activate
cd ~/database.backup
~software/database_info3.py >>~/database_info3.log
