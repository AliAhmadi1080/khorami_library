from config.celery import app
from time import sleep

@app.task
def add(x, y):
    sleep(5)
    open('log.txt', 'w').close()
    return x+y
