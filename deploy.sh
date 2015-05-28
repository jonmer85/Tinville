#!/bin/sh
if [ $PULL_REQUEST != 'false' ]; then exit 0; fi

if [ $BRANCH = 'develop' ]; then 
  heroku maintenance:on --app tinville-testing
  git push -f git@heroku.com:tinville-testing.git develop:master
  heroku run ./initDataNoInput qatest --app tinville-testing
  heroku run ./qatest collectstatic --noinput --app tinville-testing
  heroku run ./qatest compress --force --app tinville-testing
  heroku maintenance:off --app tinville-testing

  heroku maintenance:on --app tinville-dev
  git push -f git@heroku.com:tinville-dev.git develop:master
  heroku run ./initDataNoInput dev --app tinville-dev
  heroku run ./dev collectstatic --noinput --app tinville-dev
  heroku run ./dev compress --force --app tinville-dev
  heroku maintenance:off --app tinville-dev
else
  if [ $BRANCH = 'master' ]; then 
    heroku maintenance:on --app tinville-beta
    git push -f git@heroku.com:tinville-beta.git master:master
    heroku run ./initDataNoInput beta --app tinville-beta
    heroku run python manage.py collectstatic --settings=Tinville.settings.beta --noinput --app tinville-beta
    heroku run python manage.py compress --settings=Tinville.settings.beta --force --app tinville-beta
    heroku maintenance:off --app tinville-beta
  fi
fi


