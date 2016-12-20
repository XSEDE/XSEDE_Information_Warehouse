###########################################################################################
# Project layout
###########################################################################################

django_xsede_warehouse/
  xsede_warehouse/  -> The project
    glue2_db/         -> Models only
    glue2_db_api/     -> API that maps directly to the models
    glue2_views_api/  -> API with custom views
    glue2_provider/   -> Provider processing API 
    ...

###########################################################################################
# Creating a tag from a check-ou:
###########################################################################################
svn copy trunk tags/x.y-YYYYMMDD -m "Taggign to productio YYYY/MM/DD"

###########################################################################################
# PRODUCTION checkout from SVN as user 'software'
###########################################################################################
# Best practices 
#  - Tag a new version you're making production, then do a new checkout to production.
#  - Tags are just branches, to retrieve tag changes you can 'svn up'

cd /soft/warehouse-1.0
source bin/svnsetup
svn co $xdsvn/xci/source/info.warehouse/tags/tag-x.y-YYYYMMDD
cd tag-x.y-YYYYMMDD
../bin/svnfix

# Diff to previous tag, make sure the changes are expected
diff -r -x ".svn" -x "*.pyc" PROD/ tag-x.y-YYYYMMDD/

# When you are ready to switch production version
cd /soft/warehouse-1.0
ln -fs /soft/warehouse-1.0/tags/tags-x.y-YYYYMMDD PROD
cd PROD
# As root: /etc/init.d/httpd restart


###########################################################################################
# To merge back to trunk from a tag/branch (a tag becomes a branch if you commit changes to it)
###########################################################################################

svn merge --reintegrate $xdsvn/xci/source/info.warehouse/tags/tag-x.y-YYYYMMDD
