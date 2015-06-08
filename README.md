# DataWake Prefetch
DataWake prefetch scours the internet for user provided keywords, scrapes those pages and provides the user a ranked list of the website containing those keywords.

## What is the Datawake?

DataWake Prefetch is multi-tier software system consisting of client side applications (Firefox add-on), web servers (tangelo), and distributed backend platforms (kafka, storm, zookeeper, etc).

DataWake Prefetch uses a high-speed distributed crawler to find the relevant pages to your search.


# Quick Start
## Prerequisites
* [Git]( https://git-scm.com/downloads)
* [Docker]( https://docs.docker.com/)
* [Docker-Compose]( https://docs.docker.com/compose/install/)
* Working on Windows or OSX? [Boot2Docker]( http://boot2docker.io/)

Checkout DataWake Prefetch:
``` shell
$ git clone https://github.com/sotera/datawake-prefetch.git
```
Build the database:
``` shell
$ cd dev-env/
$ docker-compose up -d mysql
$ ./init-db.sh
```

Start the DataWake Prefetch containers
``` shell
$ docker-compose Build
$ docker-compose up -d
```

Now check that the Docker containers are running.
``` shell
$ docker-compose ps
Name                       Command               State           Ports
----------------------------------------------------------------------------------------
devenv_datawake_1        tangelo -c /usr/local/shar ...   Up      0.0.0.0:80->80/tcp
devenv_dwsearch_1        scala -classpath build/lib ...   Up
devenv_dwstream_1        /memex-datawake-stream/dev ...   Up
devenv_dwurlcontents_1   scala -classpath build/lib ...   Up
devenv_dwurlrank_1       scala -classpath build/lib ...   Up
devenv_mysql_1           /entrypoint.sh mysqld            Up      0.0.0.0:3336->3306/tcp
```

Run the Firefox add-on:
```shell
$ cd ../FirefoxSidebar
$ cfx run
```
