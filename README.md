# Fast API backend starter

## Usage

### With docker-compose
To run the application you need to have `Docker` and `docker-compose` installed. So, just execute from the root directory:

```bash
docker-compose up
```

So, run the first migration:

```bash
docker-compose exec app alembic upgrade head
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

## wnioski

* proste ;)

* zapierdala

* OAuth ogarniety

* pydantic sztos (poczytac doki co sie zmienilo)

## todosy

* obczaic compose

* zalozyc repo

* dodac gitlab yml

* gitignore

* env 4 vscode dev

* cleanup -> zostaje tylko auth -> update user model -> basic expandable perrmission model -> poczytac alembic o migracjach bo nie pamietam

* exception handling

* fix tests

* http files

* readme

* swagger ? jak dodac z auth

* repository pod orm proste

* example ficzer
