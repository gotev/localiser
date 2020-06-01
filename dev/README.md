# Localiser development tools
In this directory you will find the tools used during development and indications to get up and running and be part of localiser developers.

## Introduction
First of all, I assume you are working on a macOS. If you are on a different OS, it doesn't matter, but some things may be different or not working out of the box as described. In those cases, a PR with the solution will help you and other developers. Personally speaking, I can't afford debugging something I don't use.

## What you need
* patience and time
* brew
* python3
* django 2+ knowledge for Localiser UI
* your favorite editor. I use a mixture of Sublime Text and PyCharm.

## Getting started
To not mess up with your own system python packages, both `localiser-ui` and `localiser-generator` are developed in separated virtual environments. 

### Prerequisites
You need to have both python3 and virtualenv installed. On a macOS, you can install them with brew and pip3:

```
brew install python3
pip3 install virtualenv
```

### Init

Run `./init` to automatically setup the separated virtual environments for both `localiser-ui` and `localiser-generator`

## Run
to run your locally modified `localiser-ui`:

`./start-ui`

to run your locally modified `localiser-generator`:

`./generate`

this is going to use the `db.sqlite3` which is inside your local copy of `localiser-ui/db/`, so you can easily make modifications from the UI and then see the generated results in `out/` directory.

## Docker operations
### Create localiser-ui image

```
./build-docker-ui
```
the tag version is specified in `config` text file. Change it accordingly if needed.

### Run localiser-ui image
```
docker run -t -i -v $(PWD):/localiser-ui/db -p 8000:8000 gotev/localiser-ui:0.1
```

Where:

* `0.1` is the tag version to run. Change it accordingly.

* `-t -i` allows you to stop the server with `CTRL + C`

* `$(PWD)` is the path to your local directory containing the `db.sqlite3` file and `/localiser-ui/db` the internal container path to the database
* `-p 8000:8000` is the port mapping for the server. The first `8000` is your local port. You can change it as you wish. The second `8000` is the internal container server port mapping. That should always remain the same.


## Useful links
* [Reset migrations](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)
