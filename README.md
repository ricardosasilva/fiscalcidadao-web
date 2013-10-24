== Dependencies ==

* geos v3.4.2
* PostgreSQL 9.3.1
* PostGIS

== Create PostgreSQL database with PostGIS support ==

$ psql postgres
> CREATE ROLE fiscalcidadao LOGIN
  ENCRYPTED PASSWORD 'md5669aefa8077d19d1e7feffe708f905e7'
  NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;

$ createdb -W --host=127.0.0.1 --username=fiscalcidadao fiscalcidadao
$ psql --host=127.0.0.1 --username=fiscalcidadao fiscalcidadao
> CREATE EXTENSION postgis;
> CREATE EXTENSION postgis_topology;


== Importing GTFS data ==

$ python manage.py importgtfs <gtfs_data_file.zip> 
