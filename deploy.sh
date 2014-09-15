#!/bin/sh
if [ $BRANCH != 'Sprint6' ]; then exit 0; fi
git push -f git@heroku.com:tinville-testing.git Sprint6:master
./initDataNoInput qatest
./qatest collectstatic --noinput

git push -f git@heroku.com:tinville-dev.git Sprint6:master
./initDataNoInput dev
./dev collectstatic --noinput