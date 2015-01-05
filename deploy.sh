#!/bin/sh
if [ $BRANCH != 'Sprint8' ]; then exit 0; fi
if [ $PULL_REQUEST != 'false' ]; then exit 0; fi
git push -f git@heroku.com:tinville-testing.git Sprint8:master
heroku run ./initDataNoInput qatest --app tinville-testing
heroku run ./qatest collectstatic --noinput --app tinville-testing

git push -f git@heroku.com:tinville-dev.git Sprint8:master
heroku run ./initDataNoInput dev --app tinville-dev
heroku run ./dev collectstatic --noinput --app tinville-dev
