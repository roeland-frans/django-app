### Setup the local postgres database

Connect to the postgres server and create the user and database:

```shell
# Connect to the postgres container
sudo docker exec -it django_app_postgres psql -p 5432 -U postgres

# You can also use psql directly if you have it installed locally
psql -h localhost -p 5432 -U postgres
``` 

```sql
create user django with password 'django';
create database app with owner django;
```

Quite the psql shell with `\q`

### Format code

```shell
black ./django
isort ./django
```

Check code formatting:
```shell
black --check ./django
isort --check ./django
```