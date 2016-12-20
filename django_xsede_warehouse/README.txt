##########################################################################################
# Pre-requisites:
#  Python 2.7.x
#  Python pip
#  Django 1.8.x
#  Django REST framework
#  Django REST framework XML
#  Django REST swagger
#  Django jsonfield
#  Django secure
######################
######################
% sudo port install py27-pip
% sudo pip-2.7 install markdown
% sudo pip-2.7 install djangorestframework
% sudo pip-2.7 install djangorestframework-xml
% sudo pip-2.7 install django-filter
% sudo pip-2.7 install django-rest-swagger
% sudo pip-2.7 install django-jsonfield
% sudo pip-2.7 install django-secure

######################
% export PATH=/opt/local/lib/postgresql94/bin:$PATH
% alias postgres_start='sudo /opt/local/etc/LaunchDaemons/org.macports.postgresql94-server/postgresql94-server.wrapper start';
% alias postgres_stop='sudo /opt/local/etc/LaunchDaemons/org.macports.postgresql94-server/postgresql94-server.wrapper stop';
% alias postgres_restart='sudo /opt/local/etc/LaunchDaemons/org.macports.postgresql94-server/postgresql94-server.wrapper restart';

# Reference: http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

setenv PATH "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/:$PATH"
cd /Users/navarro/svn/xd/xci/source/info.warehouse/trunk

mkdir django_xsede_warehouse
django-admin.py startproject xsede_warehouse django_xsede_warehouse/
cd django_xsede_warehouse/
# edit manage.py set #!/opt/local/bin/python
manage.py startapp glue2_db
# set xsede_warehouse/settings.py DATABASES
manage.py createsuperuser
--> admin, jpfnavarro@gmail.com, djpass

python manage.py makemigrations glue2_db
python manage.py migrate glue2_db

###########################################################################################
# Database layout
#
database = warehouse
    user = warehouse_owner

  schema = django
    user = django_owner

  schema = glue2
    user = glue2_owner

###########################################################################################
# Resetting the database and django
drop schema django cascade;
drop schema glue2 cascade;
create schema django;
alter schema django owner to django_owner;
create schema glue2;
alter schema glue2 owner to glue2_owner;

manage.py migrate glue2_db zero
rm glue2_db/migrations/*.py*
./manage.py makemigrations
./manage.py migrate

###########################################################################################
# Production migration
create role [warehouse_owner, django_owner, glue2_owner, warehouse_load]

###########################################################################################

django-admin-2.7.py startproject mysite1 django.p2/
cd django.p2;django-admin-2.7.py startapp xdresources xdresources/
cd django.p2;python manage.py createsuperuser
--> admin, jpfnavarro@gmail.com, djpass

python manage.py makemigrations xdresources
python manage.py migrate xdresources
 
##############

django-admin-2.7.py startproject django_demo
django-admin-2.7.py startapp xdsoftwarecat
# set django_demo/settings.py DATABASES
python manage.py migrate
--> admin, jpfnavarro@gmail.com, djpass
# set django_demo/setting.py REST_FRAMEWORK
# set django_demo/setting.py INSTALLED_APPS rest_framework, rest_framework_swagger
python manage.py runserver
# set django_demo/setting.py INSTALLED_APPS xdsoftwarecat
# edit xdsoftwarecat/models.py
python manage.py makemigrations xdsoftwarecat
python manage.py migrate xdsoftwarecat
