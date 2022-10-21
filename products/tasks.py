from celery import shared_task

@shared_task
def adding_task(x, y):
    print("===== ADDing TASK =====")
    print(x+y)
    print("===== ===== =====")
    return x + y
