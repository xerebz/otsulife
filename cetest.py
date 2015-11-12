from celery.task import task

@task
def foo(num):
	return num + 2

celery.