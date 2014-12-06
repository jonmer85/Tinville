#!/bin/sh
if [ $BRANCH != 'Sprint8' ]; then exit 0; fi
if [ $PULL_REQUEST != 'false' ]; then exit 0; fi
git push -f git@heroku.com:tinville-testing.git Sprint8:master
./initDataNoInput qatest
./qatest collectstatic --noinput

git push -f git@heroku.com:tinville-dev.git Sprint8:master
./initDataNoInput dev
./dev collectstatic --noinput
