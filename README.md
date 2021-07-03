# Fast API backend starter
# TODO: user creation validation 4 username & email, remove items
## Usage

### With docker-compose
To run the application you need to have `Docker` and `docker-compose` installed. So, just execute from the root directory:

```bash
docker-compose up
```

#### Swagger  

```/docs```  

#### OpenAPI docs

```/redoc```  

So, run the first migration:

```bash
docker-compose exec app alembic upgrade head
```

Create migration:

```bash
docker-compose exec app alembic revision --autogenerate -m "{message}"
```

### Tests
**To run the tests:**

```
docker-compose exec app pytest
```

**To re-run the tests**, firstly, we recreate the database because there are unit tests which create resources, so if it already exists the test will fail:

Remove the data files before recreate the container
```
rm -fr db_data/*
```
Recreate the db service:

```docker
docker-compose stop db
docker-compose rm db
docker-compose up -d db
```

Finally, re-run the migration and the tests:
```
docker-compose exec app alembic upgrade head
docker-compose exec app pytest
```

<!--
### With python virtual environment
If you want to run the application from your terminal, you may create a python virtual environment, install the dependencies and run it using uvicorn:

```bash
python3 -m venv .venv
source ./venv/bin/activate
(.venv) pip install -r requirements/dev.txt
(.venv) cd backend
(.venv) uvicorn main:app --reload
```
-->


## Todoski itd

## todosy

* dodac skrypt/komende z cli aby utworzy default admin usera admin:admin

* gitlab yml

* readme

* fix tests Cucumber tests?

* example ficzer
