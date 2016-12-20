drop schema django cascade;
drop schema glue2 cascade;
create schema django;
alter schema django owner to django_owner;
create schema glue2;
alter schema glue2 owner to glue2_owner;
