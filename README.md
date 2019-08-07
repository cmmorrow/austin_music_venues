# austin_music_venues

## Getting Started

### Prerequisites

* Python 3.6 or higher
* The Conda package manager
* Docker

### Installing the Database

The database is a postgresql database running in a Docker container. To run the database, type the following commands into a command prompt:

```bash
> cd austin_music_venues/postgres
> docker build -t amvdb_postgres .
> docker run -d -p 5433:5432 -e POSTGRES_DB=amvdb --name amvdb amvdb_postgres
```

This will build the postgres image and run it with a default database called _amvdb_, as well as create the _demo_ user and _address_, _venue_, and _rating_ tables. Note that the database will be running on port 5433 instead of the default 5432. This is to avoid conflicts on port 5432 if it is already in use by another postgres instance. The amvdb database can also be logged into as the user _demo_ with no password.
