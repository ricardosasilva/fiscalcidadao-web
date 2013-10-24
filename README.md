## Dependencies

* geos v3.4.2
* PostgreSQL 9.3.1
* PostGIS


## Installing project

### Create PostgreSQL database with PostGIS support
```
$ psql postgres
> CREATE ROLE fiscalcidadao LOGIN
  ENCRYPTED PASSWORD 'md5669aefa8077d19d1e7feffe708f905e7'
  NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
  
$ createdb -W --host=127.0.0.1 --username=fiscalcidadao fiscalcidadao

$ psql --host=127.0.0.1 --username=fiscalcidadao fiscalcidadao
> CREATE EXTENSION postgis;
> CREATE EXTENSION postgis_topology;
```

### Django project

- We recommend using a [VirtualEnv](http://www.virtualenv.org/en/latest/) with
  [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

- To install requirements:

```
$ pip install -r requirements.txt
```

- If you are developing you can install the development requirements:

```
$ pip install -r requirements/dev.txt
```

- Create an settings file for you environment on fiscalcidadao/settings/dev/\<your-filename\>.py
  You can use the file fiscalcidadao/settings/dev/sample.py as a template.

- Add this file to DJANGO_SETTINGS_MODULE environment variable:

```
$ export DJANGO_SETTINGS_MODULE=fiscalcidadao.settings.dev.<your-filename>
```

## Importing GTFS data

```
$ python manage.py importgtfs <gtfs_data_file.zip> 
```
