#!/bin/bash -x

curl -s -o django_test.data \
     http://localhost:8000/xsede-api/provider/ipf-glue2/v1/location/urn:glue2:Location:TexasAdvancedComputingCenter/

epoc=`date "+%s"`

sed -i .bak "s/Texas/Chicago ${epoc}/;s/stampede.tacc/${epoc}.uchicago/" django_test.data

curl -s -X POST -o django_test.out -d @django_test.data --header "Content-Type:application/json" -u test:pass \
     http://localhost:8000/xsede-api/provider/ipf-glue2/v1/location/
