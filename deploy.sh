#!/bin/sh
[[ $BRANCH != 'Sprint6ShippableDeployments' ]] && exit 0
git push -f git@heroku.com:tinville-testing.git Sprint6:master