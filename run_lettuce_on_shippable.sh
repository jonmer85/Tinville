#!/bin/sh

if [ $BRANCH = 'feature/FastlyCache' ]; then
  git push -f git@heroku.com:tinville-lettuce.git $BRANCH:master
  heroku run ./initDataNoInput lettuce_tests_heroku --app tinville-lettuce
  heroku run ./lettuce_tests_heroku collectstatic --noinput --app tinville-lettuce
  heroku run ./lettuce_tests_heroku compress --force --app tinville-lettuce
  ./initDataNoInput lettuce_tests_heroku
  LETTUCE_TEST_SERVER='common.lettuce_extensions.DefaultSecureServer' TEST_SERVER_ADDRESS='tinville-lettuce.herokuapp.com' LETTUCE_RUN_ON_HEROKU=True coverage run --source='Tinville,basket,common,designer_shop,extensions,custom_oscar.apps.catalogue,custom_oscar.apps.checkout,custom_oscar.apps.customer,custom_oscar.apps.order,custom_oscar.apps.dashboard,user' manage.py harvest --with-xunit --xunit-file=shippable/testresults/lettucetests.xml --settings=Tinville.settings.lettuce_tests_heroku
  coverage xml -o shippable/codecoverage/coverage_lettuce.xml
  coverage run --source='Tinville,basket,common,designer_shop,extensions,custom_oscar.apps.catalogue,custom_oscar.apps.checkout,custom_oscar.apps.customer,custom_oscar.apps.order,custom_oscar.apps.dashboard,user' manage.py test --with-xunit --xunit-file=shippable/testresults/unittests.xml --settings=Tinville.settings.unit_tests
  coverage xml -o shippable/codecoverage/coverage_unittests.xml
else
  ./initDataNoInput lettuce_tests
  coverage run --source='Tinville,basket,common,designer_shop,extensions,custom_oscar.apps.catalogue,custom_oscar.apps.checkout,custom_oscar.apps.customer,custom_oscar.apps.order,custom_oscar.apps.dashboard,user' manage.py harvest --with-xunit --xunit-file=shippable/testresults/lettucetests.xml --settings=Tinville.settings.lettuce_tests
  coverage xml -o shippable/codecoverage/coverage_lettuce.xml
  coverage run --source='Tinville,basket,common,designer_shop,extensions,custom_oscar.apps.catalogue,custom_oscar.apps.checkout,custom_oscar.apps.customer,custom_oscar.apps.order,custom_oscar.apps.dashboard,user' manage.py test --with-xunit --xunit-file=shippable/testresults/unittests.xml --settings=Tinville.settings.unit_tests
  coverage xml -o shippable/codecoverage/coverage_unittests.xml
fi


