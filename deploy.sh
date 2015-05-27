#!/bin/sh
if [ $BRANCH != 'develop' ]; then exit 0; fi
if [ $PULL_REQUEST != 'false' ]; then exit 0; fi
git push -f git@heroku.com:tinville-testing.git develop:master
heroku run ./initDataNoInput qatest --app tinville-testing
heroku run ./qatest collectstatic --noinput --app tinville-testing
heroku run ./qatest compress --force --app tinville-testing

git push -f git@heroku.com:tinville-dev.git develop:master
heroku run ./initDataNoInput dev --app tinville-dev
heroku run ./dev collectstatic --noinput --app tinville-dev
heroku run ./dev compress --force --app tinville-dev
