#!/bin/sh
[[ $BRANCH != 'Sprint6' ]] && exit 0
git push -f git@heroku.com:tinville-testing.git Sprint6:master
./initDataNoInput qatest
./qatest collectstatic --noinput

git push -f git@heroku.com:tinville-dev.git Sprint6:master
./initDataNoInput dev
./dev collectstatic --noinput