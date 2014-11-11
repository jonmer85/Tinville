from celery import task


@task
def pay_designers():
    print "yo face!"