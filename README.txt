###########################################################################################
#
# XSEDE Information Services Warehouse and API
#
###########################################################################################
#
# Directory structure
#
django_xsede_warehouse/  -> The Django project
   glue2_db/             -> Models only
   glue2_db_api/         -> API that maps directly to the models
   glue2_views_api/      -> API with custom views
   glue2_provider/       -> Provider processing API 
   ...


###########################################################################################
# Creating a tag from a check-out
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


###########################################################################################
# History
###########################################################################################
# Created: Dec. 2016
# Subversion repo: https://software.xsede.org/svn/xci/source/info.warehouse/
# Reference: http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/
# Using:
#    Python 2.7.x
#    Python pip
#    Django 1.8.x
#    Django REST framework
#    Django REST framework XML
#    Django REST swagger
#    Django jsonfield
#    Django secure
# Commands:
mkdir django_xsede_warehouse
django-admin.py startproject xsede_warehouse django_xsede_warehouse/
cd django_xsede_warehouse/
# edit manage.py set #!/opt/local/bin/python
manage.py startapp glue2_db
# set xsede_warehouse/settings.py DATABASES
manage.py createsuperuser
--> admin, jpfnavarro@gmail.com, <pass>
python manage.py makemigrations glue2_db
python manage.py migrate glue2_db

#######
# Upgraded: Oct. 2019
# Git repo: https://github.com/XSEDE/XSEDE_Information_Warehouse
# Using;
#  Python 3.7.5
#  Django 2.2.6
#  etc.
